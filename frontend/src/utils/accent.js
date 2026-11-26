/**
 * 由展会标题生成稳定的色相，让卡片在没有封面图时也有辨识度。
 * 同一标题永远得到同一颜色（不随渲染顺序变化）。
 */

const HUES = [18, 32, 48, 88, 142, 168, 196, 214, 246, 280, 312, 338]

function hash(seed) {
  const text = String(seed ?? '')
  let value = 0
  for (let i = 0; i < text.length; i += 1) {
    value = (value * 31 + text.charCodeAt(i)) >>> 0
  }
  return value
}

/** 返回可直接绑定到 :style 的自定义属性对象 */
export function accentStyle(seed) {
  const hue = HUES[hash(seed) % HUES.length]
  return { '--card-hue': String(hue) }
}
