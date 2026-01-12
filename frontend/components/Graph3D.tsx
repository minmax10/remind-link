'use client'

import { useEffect, useRef, useState } from 'react'
import ForceGraph3D from 'react-force-graph-3d'
import * as THREE from 'three'
import axios from 'axios'

interface Content {
  id: string
  title: string
  url: string
  category: {
    id: string
    name: string
    color: string
  }
  source: string
  created_at: string
}

interface Category {
  id: string
  name: string
  color: string
}

interface GraphData {
  nodes: Array<{
    id: string
    name: string
    group: string
    category: string
    color: string
    url?: string
    type: 'content' | 'category'
    size: number
  }>
  links: Array<{
    source: string
    target: string
    value: number
  }>
}

const API_BASE_URL = 'http://localhost:8000'

export default function Graph3D() {
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], links: [] })
  const [loading, setLoading] = useState(true)
  const fgRef = useRef<any>()

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      // TODO: 실제 인증 토큰 사용
      const token = localStorage.getItem('access_token')
      
      const [contentsRes, categoriesRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/contents`, {
          headers: token ? { Authorization: `Bearer ${token}` } : {}
        }).catch(() => ({ data: [] })),
        axios.get(`${API_BASE_URL}/api/categories`, {
          headers: token ? { Authorization: `Bearer ${token}` } : {}
        }).catch(() => ({ data: [] }))
      ])

      const contents: Content[] = contentsRes.data || []
      const categories: Category[] = categoriesRes.data || []

      // 카테고리 노드 생성
      const categoryNodes = categories.map(cat => ({
        id: `category-${cat.id}`,
        name: cat.name,
        group: 'category',
        category: cat.id,
        color: cat.color || '#6B7280',
        type: 'category' as const,
        size: 8
      }))

      // 콘텐츠 노드 생성
      const contentNodes = contents.map((content, index) => ({
        id: `content-${content.id}`,
        name: content.title || content.url.substring(0, 30),
        group: content.category?.id || 'other',
        category: content.category?.id || 'other',
        color: content.category?.color || '#6B7280',
        url: content.url,
        type: 'content' as const,
        size: 4
      }))

      // 링크 생성 (카테고리 -> 콘텐츠)
      const links = contentNodes.map(node => ({
        source: `category-${node.category}`,
        target: node.id,
        value: 1
      }))

      setGraphData({
        nodes: [...categoryNodes, ...contentNodes],
        links
      })
      setLoading(false)
    } catch (error) {
      console.error('데이터 로딩 실패:', error)
      setLoading(false)
    }
  }

  const handleNodeClick = (node: any) => {
    if (node.type === 'content' && node.url) {
      window.open(node.url, '_blank')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-900">
        <div className="text-white text-xl">로딩 중...</div>
      </div>
    )
  }

  return (
    <div className="w-full h-screen bg-gray-900">
      <ForceGraph3D
        ref={fgRef}
        graphData={graphData}
        nodeLabel={(node: any) => node.name}
        nodeColor={(node: any) => node.color}
        nodeOpacity={0.9}
        linkColor={() => 'rgba(255, 255, 255, 0.2)'}
        linkWidth={0.5}
        linkDirectionalArrowLength={3}
        linkDirectionalArrowRelPos={1}
        linkCurvature={0.25}
        onNodeClick={handleNodeClick}
        nodeThreeObject={(node: any) => {
          // 카테고리는 더 큰 구체, 콘텐츠는 작은 구체
          const size = node.type === 'category' ? node.size : node.size / 2
          const geometry = new THREE.SphereGeometry(size, 16, 16)
          const material = new THREE.MeshPhongMaterial({
            color: node.color,
            opacity: node.type === 'category' ? 0.8 : 0.6,
            transparent: true,
            emissive: node.color,
            emissiveIntensity: 0.2
          })
          const mesh = new THREE.Mesh(geometry, material)
          
          // 카테고리 노드에 빛나는 효과 추가
          if (node.type === 'category') {
            const glowGeometry = new THREE.SphereGeometry(size * 1.2, 16, 16)
            const glowMaterial = new THREE.MeshBasicMaterial({
              color: node.color,
              transparent: true,
              opacity: 0.1
            })
            const glow = new THREE.Mesh(glowGeometry, glowMaterial)
            mesh.add(glow)
          }
          
          return mesh
        }}
        nodeThreeObjectExtend={true}
        backgroundColor="#000000"
        showNavInfo={false}
        controlType="orbit"
        enableNodeDrag={false}
        cooldownTicks={100}
        warmupTicks={100}
        onEngineStop={() => {
          if (fgRef.current) {
            fgRef.current.zoomToFit(400, 20)
          }
        }}
        // 조명 추가
        onRenderFramePre={(scene: any) => {
          if (!scene.userData.lightsAdded) {
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
            scene.add(ambientLight)
            
            const directionalLight1 = new THREE.DirectionalLight(0xffffff, 0.8)
            directionalLight1.position.set(1, 1, 1)
            scene.add(directionalLight1)
            
            const directionalLight2 = new THREE.DirectionalLight(0xffffff, 0.4)
            directionalLight2.position.set(-1, -1, -1)
            scene.add(directionalLight2)
            
            scene.userData.lightsAdded = true
          }
        }}
      />
      
      {/* 컨트롤 패널 */}
      <div className="absolute top-4 left-4 bg-black/50 backdrop-blur-sm rounded-lg p-4 text-white">
        <h2 className="text-xl font-bold mb-2">Remind Link 3D Graph</h2>
        <p className="text-sm text-gray-300">
          노드 클릭: 콘텐츠 열기<br/>
          드래그: 회전<br/>
          스크롤: 줌
        </p>
        <div className="mt-4">
          <div className="text-sm">
            <div>노드 수: {graphData.nodes.length}</div>
            <div>링크 수: {graphData.links.length}</div>
          </div>
        </div>
      </div>
    </div>
  )
}

