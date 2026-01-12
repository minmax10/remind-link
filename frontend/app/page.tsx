'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Content {
  id: string
  title: string
  url: string
  description: string
  image_url: string
  category: {
    id: string
    name: string
    color: string
  }
  source: string
  created_at: string
}

export default function Home() {
  const [contents, setContents] = useState<Content[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [showConnectModal, setShowConnectModal] = useState(false)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [connecting, setConnecting] = useState(false)

  useEffect(() => {
    const storedToken = localStorage.getItem('access_token')
    setToken(storedToken)
    if (storedToken) {
      fetchContents(storedToken)
    } else {
      setLoading(false)
    }
  }, [])

  const fetchContents = async (authToken: string) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/contents`, {
        headers: { Authorization: `Bearer ${authToken}` }
      })
      setContents(response.data || [])
      setLoading(false)
    } catch (err: any) {
      setError(err.response?.data?.detail || '콘텐츠를 불러오는데 실패했습니다')
      setLoading(false)
    }
  }

  const handleInstagramConnect = async () => {
    if (!username || !password) {
      setError('사용자명과 비밀번호를 입력해주세요')
      return
    }
    
    try {
      setConnecting(true)
      setError(null)
      const response = await axios.post(
        `${API_BASE_URL}/api/integrations/instagram/connect`,
        { username, password },
        { headers: token ? { Authorization: `Bearer ${token}` } : {} }
      )
      setShowConnectModal(false)
      setUsername('')
      setPassword('')
      alert('인스타그램 연동이 완료되었습니다! 동기화 버튼을 눌러 저장된 게시물을 가져오세요.')
    } catch (err: any) {
      setError(err.response?.data?.detail || '인스타그램 연동에 실패했습니다')
    } finally {
      setConnecting(false)
    }
  }

  const handleSync = async () => {
    if (!token) return
    try {
      setLoading(true)
      setError(null)
      // 연동 목록 조회
      const integrationsRes = await axios.get(
        `${API_BASE_URL}/api/integrations`,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      
      const instagramIntegration = integrationsRes.data.find(
        (i: any) => i.platform === 'instagram' && i.is_active
      )
      
      if (instagramIntegration) {
        // 동기화 실행
        await axios.post(
          `${API_BASE_URL}/api/integrations/${instagramIntegration.id}/sync`,
          {},
          { headers: { Authorization: `Bearer ${token}` } }
        )
        // 콘텐츠 다시 불러오기
        await fetchContents(token)
        alert('동기화가 완료되었습니다!')
      } else {
        setError('인스타그램 연동이 필요합니다')
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || '동기화에 실패했습니다')
      setLoading(false)
    }
  }

  if (!token) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
        <div className="bg-white p-8 rounded-lg shadow-md text-center max-w-md w-full">
          <h1 className="text-3xl font-bold mb-4">Remind Link</h1>
          <p className="text-gray-600 mb-6">로그인이 필요합니다</p>
          <a 
            href="/login"
            className="inline-block bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition-colors"
          >
            로그인 페이지로 이동 →
          </a>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h1 className="text-3xl font-bold mb-4">Remind Link</h1>
          <p className="text-gray-600 mb-6">
            인스타그램에 저장한 게시물을 자동으로 가져와서 정리해드립니다
          </p>
          
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <h2 className="font-semibold text-blue-900 mb-2">📌 사용 방법</h2>
            <ol className="list-decimal list-inside space-y-1 text-sm text-blue-800">
              <li>"인스타그램 연동" 버튼을 클릭하세요</li>
              <li>인스타그램 사용자명과 비밀번호를 입력하세요</li>
              <li>"동기화" 버튼을 눌러 저장된 게시물을 가져오세요</li>
            </ol>
            <p className="text-xs text-blue-700 mt-2">
              ⚠️ 2단계 인증이 활성화된 경우 앱 비밀번호를 사용하세요
            </p>
          </div>

          <div className="flex gap-4">
            <button
              onClick={() => setShowConnectModal(true)}
              className="bg-pink-600 text-white px-6 py-3 rounded-lg hover:bg-pink-700 transition-colors font-semibold"
            >
              📸 인스타그램 연동
            </button>
            <button
              onClick={handleSync}
              disabled={loading}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors font-semibold"
            >
              {loading ? '동기화 중...' : '🔄 동기화'}
            </button>
          </div>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {showConnectModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-md w-full">
              <h2 className="text-2xl font-bold mb-4">인스타그램 연동</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1">사용자명</label>
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="w-full px-3 py-2 border rounded"
                    placeholder="인스타그램 사용자명"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">비밀번호</label>
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full px-3 py-2 border rounded"
                    placeholder="인스타그램 비밀번호"
                  />
                </div>
                <div className="text-sm text-gray-600">
                  ⚠️ 2단계 인증이 활성화된 경우 앱 비밀번호를 사용하세요
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={handleInstagramConnect}
                    disabled={connecting}
                    className="flex-1 bg-pink-600 text-white px-4 py-2 rounded hover:bg-pink-700 disabled:bg-gray-400"
                  >
                    {connecting ? '연동 중...' : '연동하기'}
                  </button>
                  <button
                    onClick={() => {
                      setShowConnectModal(false)
                      setUsername('')
                      setPassword('')
                      setError(null)
                    }}
                    className="flex-1 bg-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-400"
                  >
                    취소
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {loading && contents.length === 0 ? (
          <div className="text-center py-8">로딩 중...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {contents.map((content) => (
              <div
                key={content.id}
                className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
              >
                {content.image_url && (
                  <img
                    src={content.image_url}
                    alt={content.title}
                    className="w-full h-48 object-cover"
                    onError={(e) => {
                      (e.target as HTMLImageElement).style.display = 'none'
                    }}
                  />
                )}
                <div className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <span
                      className="px-2 py-1 rounded text-xs text-white"
                      style={{ backgroundColor: content.category?.color || '#6B7280' }}
                    >
                      {content.category?.name || '기타'}
                    </span>
                    <span className="text-xs text-gray-500">{content.source}</span>
                  </div>
                  <h3 className="font-bold text-lg mb-2 line-clamp-2">
                    {content.title || '제목 없음'}
                  </h3>
                  {content.description && (
                    <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                      {content.description}
                    </p>
                  )}
                  <a
                    href={content.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline text-sm"
                  >
                    링크 열기 →
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}

        {!loading && contents.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            저장된 콘텐츠가 없습니다. 인스타그램을 연동하고 동기화해보세요.
          </div>
        )}
      </div>
    </div>
  )
}
