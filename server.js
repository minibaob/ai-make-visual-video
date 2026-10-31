// 本地 Web 配置台服务器
// 用法：node server.js [端口]  默认 3000
const http = require('http');
const fs = require('fs');
const path = require('path');
const { exec, spawn } = require('child_process');

const ROOT = __dirname;
const PORT = parseInt(process.argv[2] || '3000', 10);

// 读取配置
function loadConfig() {
  return JSON.parse(fs.readFileSync(path.join(ROOT, 'config.json'), 'utf8'));
}
function saveConfig(cfg) {
  fs.writeFileSync(path.join(ROOT, 'config.json'), JSON.stringify(cfg, null, 2));
}

// 执行 CLI 命令，返回结果
function runCli(args) {
  return new Promise((resolve) => {
    const child = spawn('node', ['cli.js', ...args], { cwd: ROOT });
    let out = '', err = '';
    child.stdout.on('data', d => out += d);
    child.stderr.on('data', d => err += d);
    child.on('close', code => resolve({ code, out, err }));
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);

  // CORS + JSON 工具
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }

  // 静态文件
  if (req.method === 'GET' && url.pathname === '/') {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(fs.readFileSync(path.join(ROOT, 'config.html')));
    return;
  }

  // API: 获取配置
  if (req.method === 'GET' && url.pathname === '/api/config') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify(loadConfig()));
    return;
  }

  // API: 保存配置
  if (req.method === 'POST' && url.pathname === '/api/config') {
    let body = '';
    req.on('data', d => body += d);
    req.on('end', () => {
      try {
        const cfg = JSON.parse(body);
        saveConfig(cfg);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true }));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, error: e.message }));
      }
    });
    return;
  }

  // API: 执行命令（render / cover / music / list）
  if (req.method === 'POST' && url.pathname === '/api/run') {
    let body = '';
    req.on('data', d => body += d);
    req.on('end', async () => {
      try {
        const { command, args } = JSON.parse(body);
        const result = await runCli([command, ...(args || [])]);
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify(result));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, error: e.message }));
      }
    });
    return;
  }

  res.writeHead(404); res.end('Not Found');
});

server.listen(PORT, () => {
  console.log(`\n数学可视化视频配置台已启动:`);
  console.log(`  打开浏览器访问 http://localhost:${PORT}\n`);
});
