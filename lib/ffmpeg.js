// 自动定位 ffmpeg 可执行文件
// 优先级：环境变量 FFMPEG > 常见路径 > imageio-ffmpeg 包 > 系统 PATH
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

function exists(p) { try { return fs.existsSync(p); } catch { return false; } }

function findFfmpeg() {
  // 1. 环境变量
  if (process.env.FFMPEG && exists(process.env.FFMPEG)) return process.env.FFMPEG;

  const candidates = [];

  // 2. imageio-ffmpeg 包（Python 安装后自带）
  try {
    const py = execSync('python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"', { encoding: 'utf8' }).trim();
    if (py && exists(py)) candidates.push(py);
  } catch {}

  // 3. 常见 Windows 路径（WorkBuddy 环境）
  const home = process.env.USERPROFILE || process.env.HOME || 'C:/Users/Default';
  const glob = (dir) => {
    try {
      if (!exists(dir)) return [];
      return fs.readdirSync(dir).filter(f => f.includes('ffmpeg'));
    } catch { return []; }
  };
  // imageio-ffmpeg 常见安装位置
  const pyDirs = [];
  try {
    const base = path.join(home, '.workbuddy', 'binaries', 'python', 'versions');
    if (exists(base)) {
      for (const v of fs.readdirSync(base)) {
        const site = path.join(base, v, 'Lib', 'site-packages', 'imageio_ffmpeg', 'binaries');
        for (const f of glob(site)) candidates.push(path.join(site, f));
      }
    }
  } catch {}

  // 4. 系统 PATH
  try {
    const which = execSync('where ffmpeg 2>nul || which ffmpeg 2>/dev/null', { encoding: 'utf8' }).trim().split('\n')[0];
    if (which && exists(which)) candidates.push(which);
  } catch {}

  for (const c of candidates) {
    if (exists(c)) return c;
  }
  return null;
}

module.exports = { findFfmpeg };
