import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Remind Link - 3D Graph View',
  description: '인스타그램과 쓰레드 저장글을 3D 그래프로 시각화',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko">
      <body className="antialiased">{children}</body>
    </html>
  )
}
