/**
 * 数据看板模块 — Chart.js 图表渲染
 */
window.Dashboard = (() => {
  let revenueChart = null;
  let roomTypeChart = null;

  const roomTypeLabels = { single: "单间", suite: "套房", whole: "整栋" };
  // 与 Refined Nature 设计系统对齐的图表配色
  const chartColors = ["#4A7C59", "#C67A4B", "#3B8C7A", "#D4953A", "#2D4A38", "#8FA195"];

  async function load() {
    try {
      const stats = await API.get("dashboard/stats");
      renderStats(stats);
      renderCharts(stats);
    } catch (err) {
      toast("加载统计数据失败: " + err.message, "error");
    }
  }

  function renderStats(s) {
    document.getElementById("stat-revenue").textContent = `¥${s.total_revenue.toLocaleString()}`;
    document.getElementById("stat-monthly").textContent = `¥${s.monthly_revenue.toLocaleString()}`;
    document.getElementById("stat-occupancy").textContent = `${(s.occupancy_rate * 100).toFixed(1)}%`;
    document.getElementById("stat-bookings").textContent = s.total_bookings;
  }

  function renderCharts(s) {
    renderRevenueTrend(s.revenue_trend);
    renderRoomTypeDist(s.room_type_distribution);
  }

  function renderRevenueTrend(trend) {
    const ctx = document.getElementById("revenue-chart");
    if (revenueChart) revenueChart.destroy();
    revenueChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: trend.map((t) => t.date.slice(5)),
        datasets: [{
          label: "收益 (¥)",
          data: trend.map((t) => t.revenue),
          borderColor: "#4A7C59",
          backgroundColor: "rgba(74, 124, 89, 0.12)",
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointBackgroundColor: "#4A7C59",
          pointHoverRadius: 6,
        }],
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, ticks: { callback: (v) => "¥" + v } },
        },
      },
    });
  }

  function renderRoomTypeDist(dist) {
    const ctx = document.getElementById("room-type-chart");
    if (roomTypeChart) roomTypeChart.destroy();
    const labels = Object.keys(dist).map((k) => roomTypeLabels[k] || k);
    const values = Object.values(dist);
    roomTypeChart = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels,
        datasets: [{
          data: values,
          backgroundColor: chartColors.slice(0, labels.length),
          borderWidth: 0,
        }],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "bottom", labels: { padding: 16, usePointStyle: true } },
        },
      },
    });
  }

  return { load };
})();
