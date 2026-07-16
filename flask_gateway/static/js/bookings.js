/**
 * 预订管理模块
 */
window.Bookings = (() => {
  const statusLabels = {
    pending: "待确认",
    confirmed: "已确认",
    checked_in: "已入住",
    checked_out: "已退房",
    cancelled: "已取消",
  };
  const statusClass = {
    pending: "badge-pending",
    confirmed: "badge-confirmed",
    checked_in: "badge-checked_in",
    checked_out: "badge-checked_out",
    cancelled: "badge-cancelled",
  };
  const nextActions = {
    pending: [{ label: "确认", status: "confirmed", cls: "btn-success" }],
    confirmed: [
      { label: "入住", status: "checked_in", cls: "btn-primary" },
      { label: "取消", status: "cancelled", cls: "btn-danger" },
    ],
    checked_in: [{ label: "退房", status: "checked_out", cls: "btn-outline" }],
    checked_out: [],
    cancelled: [],
  };

  let statusFilter = "";

  async function load() {
    const qs = statusFilter ? `?status=${statusFilter}` : "";
    const list = await API.get(`bookings${qs}`);
    render(list);
  }

  function render(bookings) {
    const tbody = document.getElementById("booking-list");
    if (!bookings.length) {
      tbody.innerHTML = `<tr><td colspan="9" style="text-align:center;padding:2rem;color:var(--gray-500)">暂无预订数据</td></tr>`;
      return;
    }
    tbody.innerHTML = bookings.map((b) => `
      <tr>
        <td>#${b.id}</td>
        <td>${b.room_name || "—"}</td>
        <td>${b.guest_name}<br><small style="color:var(--gray-500)">${b.guest_phone || ""}</small></td>
        <td>${b.check_in}</td>
        <td>${b.check_out}</td>
        <td>${b.nights}</td>
        <td><strong>¥${b.total_price}</strong></td>
        <td><span class="badge ${statusClass[b.status]}">${statusLabels[b.status] || b.status}</span></td>
        <td>${actionButtons(b)}</td>
      </tr>
    `).join("");
  }

  function actionButtons(b) {
    const actions = nextActions[b.status] || [];
    return actions.map(
      (a) => `<button class="btn ${a.cls} btn-sm" onclick="Bookings.changeStatus(${b.id}, '${a.status}')">${a.label}</button>`
    ).join(" ") || "—";
  }

  function openCreateModal() {
    const today = new Date().toISOString().split("T")[0];
    const html = `
      <form id="booking-form">
        <div class="form-group">
          <label>房源 ID</label>
          <input name="room_id" type="number" required min="1" placeholder="输入房源 ID（可在房源管理页查看）">
        </div>
        <div class="form-group">
          <label>客人姓名</label>
          <input name="guest_name" required placeholder="入住人姓名">
        </div>
        <div class="form-group">
          <label>联系电话</label>
          <input name="guest_phone" placeholder="选填">
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>入住日期</label>
            <input name="check_in" type="date" required min="${today}">
          </div>
          <div class="form-group">
            <label>退房日期</label>
            <input name="check_out" type="date" required min="${today}">
          </div>
        </div>
        <div class="form-group">
          <label>备注</label>
          <textarea name="remark" rows="2" placeholder="选填"></textarea>
        </div>
      </form>
    `;
    Modal.open("新增预订", html, async () => {
      const form = document.getElementById("booking-form");
      const fd = new FormData(form);
      const checkIn = fd.get("check_in");
      const checkOut = fd.get("check_out");
      if (checkOut <= checkIn) {
        toast("退房日期必须晚于入住日期", "error");
        return;
      }
      const payload = {
        room_id: Number(fd.get("room_id")),
        guest_name: fd.get("guest_name"),
        guest_phone: fd.get("guest_phone"),
        check_in: checkIn,
        check_out: checkOut,
        remark: fd.get("remark"),
      };
      try {
        await API.post("bookings", payload);
        toast("预订创建成功", "success");
        load();
      } catch (err) {
        toast(err.message, "error");
      }
    });
  }

  async function changeStatus(id, status) {
    try {
      await API.put(`bookings/${id}`, { status });
      toast("状态已更新", "success");
      load();
    } catch (err) {
      toast(err.message, "error");
    }
  }

  // 事件
  document.getElementById("btn-add-booking").addEventListener("click", openCreateModal);
  document.getElementById("booking-status-filter").addEventListener("change", (e) => {
    statusFilter = e.target.value;
    load();
  });

  return { load, changeStatus };
})();
