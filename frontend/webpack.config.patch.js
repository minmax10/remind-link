// webpack 설정 패치 - three-render-objects의 webgpu 문제 해결
// 이 파일은 참고용이며, 실제 설정은 next.config.js에 포함되어 있습니다.

module.exports = function patchWebpackConfig(config) {
  // three-render-objects에서 webgpu import를 무시
  config.resolve = config.resolve || {}
  config.resolve.alias = {
    ...config.resolve.alias,
    'three/webgpu': false,
  }
  
  // 모듈 규칙 추가
  config.module = config.module || {}
  config.module.rules = config.module.rules || []
  
  return config
}
