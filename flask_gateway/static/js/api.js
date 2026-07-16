/**
 * 统一 API 请求封装
 * - 自动附带 JWT Authorization header
 * - 统一错误处理
 * - 所有请求走 Flask 网关 /api 前缀
 */
const API = (() => {
  const TOKEN_KEY = "bnb_token";
  const USER_KEY = "bnb_user";

  function getToken() {
    return localStorage.getItem(TOKEN_KEY);
  }

  function getUser() {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  }

  function setAuth(token, user) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  function clearAuth() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }

  async function request(method, path, body) {
    const headers = { "Content-Type": "application/json" };
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const res = await fetch(`/api/${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });

    if (res.status === 204) return null;

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      const msg = data.detail || `请求失败 (${res.status})`;
      throw new Error(msg);
    }
    return data;
  }

  return {
    getToken,
    getUser,
    setAuth,
    clearAuth,
    get: (p) => request("GET", p),
    post: (p, b) => request("POST", p, b),
    put: (p, b) => request("PUT", p, b),
    del: (p) => request("DELETE", p),
  };
})();

/* ========== Toast 提示 ========== */
function toast(message, type = "info") {
  const container = document.getElementById("toast-container");
  const el = document.createElement("div");
  el.className = `toast toast-${type}`;
  const icons = { success: "✓", error: "✕", warning: "!", info: "i" };
  el.innerHTML = `<span style="font-weight:700">${icons[type] || "i"}</span><span>${message}</span>`;
  container.appendChild(el);
  setTimeout(() => {
    el.style.opacity = "0";
    el.style.transform = "translateX(100%)";
    el.style.transition = "all 0.3s";
    setTimeout(() => el.remove(), 300);
  }, 3000);
}

/* ========== Modal 通用弹窗 ========== */
const Modal = (() => {
  const modal = document.getElementById("modal");
  const title = document.getElementById("modal-title");
  const body = document.getElementById("modal-body");

  function open(titleText, contentHtml, onConfirm) {
    title.textContent = titleText;
    body.innerHTML = contentHtml;

    if (onConfirm) {
      const footer = document.createElement("div");
      footer.className = "modal-footer";
      footer.innerHTML = `
        <button class="btn btn-outline" id="modal-cancel">取消</button>
        <button class="btn btn-primary" id="modal-confirm">确定</button>
      `;
      body.appendChild(footer);
      document.getElementById("modal-cancel").onclick = close;
      document.getElementById("modal-confirm").onclick = () => {
        onConfirm();
        close();
      };
    }

    modal.classList.remove("hidden");
  }

  function close() {
    modal.classList.add("hidden");
    body.innerHTML = "";
  }

  document.getElementById("modal-close").onclick = close;
  document.querySelector(".modal-mask").onclick = close;

  return { open, close };
})();
