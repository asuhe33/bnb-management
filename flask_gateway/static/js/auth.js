/**
 * 认证模块：登录/注册/路由守卫
 */
(function () {
  const authPage = document.getElementById("auth-page");
  const app = document.getElementById("app");

  // Tab 切换
  document.querySelectorAll(".auth-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".auth-tab").forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
      const which = tab.dataset.tab;
      document.getElementById("login-form").classList.toggle("hidden", which !== "login");
      document.getElementById("register-form").classList.toggle("hidden", which !== "register");
    });
  });

  // 登录
  document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    try {
      const data = await API.post("auth/login", {
        username: form.get("username"),
        password: form.get("password"),
      });
      API.setAuth(data.access_token, data.user);
      toast("登录成功", "success");
      enterApp();
    } catch (err) {
      toast(err.message, "error");
    }
  });

  // 注册
  document.getElementById("register-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    try {
      const data = await API.post("auth/register", {
        username: form.get("username"),
        password: form.get("password"),
        full_name: form.get("full_name"),
      });
      API.setAuth(data.access_token, data.user);
      toast("注册成功", "success");
      enterApp();
    } catch (err) {
      toast(err.message, "error");
    }
  });

  // 退出
  document.getElementById("logout-btn").addEventListener("click", () => {
    API.clearAuth();
    location.hash = "";
    location.reload();
  });

  function enterApp() {
    authPage.classList.add("hidden");
    app.classList.remove("hidden");
    const user = API.getUser();
    document.getElementById("user-name").textContent = user?.full_name || user?.username || "";
    navigate(location.hash || "#/dashboard");
  }

  // 路由
  window.addEventListener("hashchange", () => navigate(location.hash));

  function navigate(hash) {
    const route = hash.replace("#", "") || "/dashboard";
    document.querySelectorAll(".view").forEach((v) => v.classList.add("hidden"));
    const viewMap = {
      "/dashboard": "view-dashboard",
      "/rooms": "view-rooms",
      "/bookings": "view-bookings",
    };
    const viewId = viewMap[route] || "view-dashboard";
    document.getElementById(viewId).classList.remove("hidden");

    document.querySelectorAll(".nav-item").forEach((n) => {
      n.classList.toggle("active", n.dataset.route === route.replace("/", ""));
    });

    // 触发页面加载
    if (route === "/dashboard") window.Dashboard?.load();
    if (route === "/rooms") window.Rooms?.load();
    if (route === "/bookings") window.Bookings?.load();
  }

  window.__navigate = navigate;

  // 初始化：已登录则直接进入
  if (API.getToken()) {
    enterApp();
  }
})();
