/**
 * 房源管理模块
 */
window.Rooms = (() => {
  const roomTypeLabels = { single: "单间", suite: "套房", whole: "整栋" };
  const roomIcons = { single: "🏠", suite: "🛏️", whole: "🏡" };
  let keyword = "";

  async function load() {
    const list = await API.get(`rooms?keyword=${encodeURIComponent(keyword)}`);
    render(list);
  }

  function render(rooms) {
    const container = document.getElementById("room-list");
    if (!rooms.length) {
      container.innerHTML = `<div class="empty-state" style="grid-column:1/-1">暂无房源，点击"新增房源"开始添加</div>`;
      return;
    }
    container.innerHTML = rooms.map((r) => `
      <div class="room-card">
        <div class="room-card-img">${roomIcons[r.type] || "🏠"}</div>
        <div class="room-card-body">
          <div class="room-card-title">${r.name}</div>
          <div class="room-card-meta">
            <span>${roomTypeLabels[r.type] || r.type}</span>
            <span>可住 ${r.capacity} 人</span>
            <span class="badge badge-${r.status === "available" ? "available" : "maintenance"}">${
              r.status === "available" ? "可预订" : "维护中"
            }</span>
          </div>
          <div class="room-card-price">¥${r.price} <small style="color:var(--gray-500);font-weight:400">/ 晚</small></div>
          <div class="room-card-actions">
            <button class="btn btn-outline btn-sm" onclick="Rooms.editRoom(${r.id})">编辑</button>
            <button class="btn btn-danger btn-sm" onclick="Rooms.deleteRoom(${r.id})">删除</button>
          </div>
        </div>
      </div>
    `).join("");
  }

  function openModal(room) {
    const isEdit = !!room;
    const html = `
      <form id="room-form">
        <div class="form-group">
          <label>房源名称</label>
          <input name="name" required value="${room?.name || ""}" placeholder="例如·山景小屋">
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>房型</label>
            <select name="type" required>
              <option value="single" ${room?.type === "single" ? "selected" : ""}>单间</option>
              <option value="suite" ${room?.type === "suite" ? "selected" : ""}>套房</option>
              <option value="whole" ${room?.type === "whole" ? "selected" : ""}>整栋</option>
            </select>
          </div>
          <div class="form-group">
            <label>价格(元/晚)</label>
            <input name="price" type="number" required min="1" value="${room?.price || ""}">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>可住人数</label>
            <input name="capacity" type="number" min="1" max="20" value="${room?.capacity || 2}">
          </div>
          <div class="form-group">
            <label>状态</label>
            <select name="status">
              <option value="available" ${room?.status !== "maintenance" ? "selected" : ""}>可预订</option>
              <option value="maintenance" ${room?.status === "maintenance" ? "selected" : ""}>维护中</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label>设施(逗号分隔)</label>
          <input name="amenities" value="${(room?.amenities || []).join(", ")}" placeholder="WiFi, 空调, 独立卫浴">
        </div>
        <div class="form-group">
          <label>简介</label>
          <textarea name="description" rows="2">${room?.description || ""}</textarea>
        </div>
      </form>
    `;

    Modal.open(isEdit ? "编辑房源" : "新增房源", html, async () => {
      const form = document.getElementById("room-form");
      const fd = new FormData(form);
      const payload = {
        name: fd.get("name"),
        type: fd.get("type"),
        price: Number(fd.get("price")),
        capacity: Number(fd.get("capacity")),
        status: fd.get("status"),
        amenities: fd.get("amenities").split(/[,，]/).map((s) => s.trim()).filter(Boolean),
        description: fd.get("description"),
      };
      try {
        if (isEdit) {
          await API.put(`rooms/${room.id}`, payload);
          toast("更新成功", "success");
        } else {
          await API.post("rooms", payload);
          toast("创建成功", "success");
        }
        load();
      } catch (err) {
        toast(err.message, "error");
      }
    });
  }

  async function editRoom(id) {
    const room = await API.get(`rooms/${id}`);
    openModal(room);
  }

  function deleteRoom(id) {
    Modal.open("确认删除", `<p>确定要删除该房源吗？此操作不可恢复。</p>`, async () => {
      try {
        await API.del(`rooms/${id}`);
        toast("已删除", "success");
        load();
      } catch (err) {
        toast(err.message, "error");
      }
    });
  }

  // 事件绑定
  document.getElementById("btn-add-room").addEventListener("click", () => openModal(null));
  document.getElementById("btn-room-search").addEventListener("click", () => {
    keyword = document.getElementById("room-search").value.trim();
    load();
  });
  document.getElementById("room-search").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      keyword = e.target.value.trim();
      load();
    }
  });

  return { load, editRoom, deleteRoom };
})();
