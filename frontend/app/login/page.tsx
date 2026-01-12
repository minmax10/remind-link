'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function LoginPage() {
  const router = useRouter()
  const [isLogin, setIsLogin] = useState(true)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    e.stopPropagation()
    
    // 입력값 검증
    if (!name || !name.trim()) {
      setError('이름을 입력해주세요')
      return
    }
    if (!email || !email.trim()) {
      setError('이메일을 입력해주세요')
      return
    }
    if (!password || password.length < 4) {
      setError('비밀번호는 최소 4자 이상이어야 합니다')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/auth/register`,
        {
          email: email.trim(),
          password: password,
          name: name.trim()
        },
        {
          headers: {
            'Content-Type': 'application/json'
          },
          timeout: 10000
        }
      )
      
      // 회원가입 성공 후 자동 로그인
      const formData = new URLSearchParams()
      formData.append('username', email.trim())
      formData.append('password', password)

      const loginResponse = await axios.post(
        `${API_BASE_URL}/api/auth/login`,
        formData,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          timeout: 10000
        }
      )

      // 토큰 저장
      localStorage.setItem('access_token', loginResponse.data.access_token)
      
      // 메인 페이지로 이동
      router.push('/')
    } catch (err: any) {
      console.error('회원가입 오류 상세:', {
        message: err.message,
        response: err.response?.data,
        status: err.response?.status,
        code: err.code
      })
      
      let errorMessage = '회원가입에 실패했습니다'
      
      if (err.code === 'ECONNREFUSED' || err.message?.includes('Network Error')) {
        errorMessage = '서버에 연결할 수 없습니다. 백엔드 서버가 실행 중인지 확인해주세요.'
      } else if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail
      } else if (err.message) {
        errorMessage = err.message
      }
      
      setError(errorMessage)
      setLoading(false)
    }
  }

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      // form-data 형식으로 전송
      const formData = new URLSearchParams()
      formData.append('username', email)
      formData.append('password', password)

      const response = await axios.post(
        `${API_BASE_URL}/api/auth/login`,
        formData,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      )

      // 토큰 저장
      localStorage.setItem('access_token', response.data.access_token)
      
      // 메인 페이지로 이동
      router.push('/')
    } catch (err: any) {
      setError(err.response?.data?.detail || '로그인에 실패했습니다')
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-md p-8 max-w-md w-full">
        <h1 className="text-3xl font-bold mb-6 text-center">Remind Link</h1>
        
        <div className="flex gap-4 mb-6">
          <button
            type="button"
            onClick={(e) => {
              e.preventDefault()
              e.stopPropagation()
              console.log('로그인 탭 클릭')
              setIsLogin(true)
              setError(null)
              setEmail('')
              setPassword('')
              setName('')
            }}
            className={`flex-1 py-2 rounded transition-colors cursor-pointer ${
              isLogin
                ? 'bg-blue-600 text-white font-semibold'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
            style={{ pointerEvents: 'auto' }}
          >
            로그인
          </button>
          <button
            type="button"
            onClick={(e) => {
              e.preventDefault()
              e.stopPropagation()
              console.log('회원가입 탭 클릭')
              setIsLogin(false)
              setError(null)
              setEmail('')
              setPassword('')
              setName('')
            }}
            className={`flex-1 py-2 rounded transition-colors cursor-pointer ${
              !isLogin
                ? 'bg-blue-600 text-white font-semibold'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
            style={{ pointerEvents: 'auto' }}
          >
            회원가입
          </button>
        </div>
        
        {/* 디버깅용: 현재 모드 표시 */}
        <div className="mb-4 text-center text-xs text-gray-500">
          현재 모드: {isLogin ? '로그인' : '회원가입'}
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            <p className="font-semibold">오류 발생</p>
            <p>{error}</p>
            <p className="text-xs mt-2 text-red-600">
              💡 브라우저 개발자 도구(F12) → Console 탭에서 자세한 오류를 확인하세요
            </p>
          </div>
        )}

        {!isLogin ? (
          <form 
            onSubmit={handleRegister}
            noValidate
            key="register-form"
          >
            <div className="mb-4">
              <label className="block text-sm font-medium mb-1">이름 *</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="이름을 입력하세요"
                required
                disabled={loading}
                autoComplete="name"
              />
            </div>
            
            <div className="mb-4">
              <label className="block text-sm font-medium mb-1">이메일 *</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="이메일을 입력하세요"
                required
                disabled={loading}
                autoComplete="email"
              />
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium mb-1">비밀번호 *</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="비밀번호를 입력하세요 (최소 4자)"
                required
                minLength={4}
                disabled={loading}
                autoComplete="new-password"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-semibold transition-colors"
            >
              {loading ? '처리 중...' : '회원가입'}
            </button>
          </form>
        ) : (
          <form 
            onSubmit={handleLogin}
            noValidate
            key="login-form"
          >
            <div className="mb-4">
              <label className="block text-sm font-medium mb-1">이메일 *</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="이메일을 입력하세요"
                required
                disabled={loading}
                autoComplete="email"
              />
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium mb-1">비밀번호 *</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="비밀번호를 입력하세요"
                required
                disabled={loading}
                autoComplete="current-password"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-semibold transition-colors"
            >
              {loading ? '처리 중...' : '로그인'}
            </button>
          </form>
        )}

        <div className="mt-6 text-center text-sm text-gray-600">
          <p>Swagger는 API 테스트 도구입니다.</p>
          <p>이 페이지에서 직접 로그인하시면 됩니다.</p>
        </div>
      </div>
    </div>
  )
}
