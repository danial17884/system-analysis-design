// statistics.js

document.addEventListener("DOMContentLoaded", () => {
  // تنظیمات کلی برای هماهنگی با تم تاریک پروژه
  Chart.defaults.color = "#a0a0a0";
  Chart.defaults.font.family = "Vazirmatn";

  // ۱. نمودار خطی (روند مالی ماه‌ها)
  const trendCtx = document.getElementById("trendChart");
  if (trendCtx) {
    new Chart(trendCtx, {
      type: "line",
      data: {
        labels: ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور"],
        datasets: [
          {
            label: "درآمد",
            data: [12, 19, 15, 22, 30, 28],
            borderColor: "#2ecc71", // سبز
            backgroundColor: "rgba(46, 204, 113, 0.1)",
            tension: 0.4,
            fill: true,
          },
          {
            label: "هزینه",
            data: [8, 12, 10, 15, 20, 18],
            borderColor: "#ff7a00", // نارنجی تم شما
            backgroundColor: "rgba(255, 122, 0, 0.1)",
            tension: 0.4,
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "top" },
        },
        scales: {
          y: { grid: { color: "#2a2a2a" } },
          x: { grid: { color: "#2a2a2a" } },
        },
      },
    });
  }

  // ۲. نمودار دونات (دسته‌بندی هزینه‌ها)
  const categoryCtx = document.getElementById("categoryChart");
  if (categoryCtx) {
    new Chart(categoryCtx, {
      type: "doughnut",
      data: {
        labels: ["خوراک", "حمل و نقل", "سرگرمی", "قبوض", "سایر"],
        datasets: [
          {
            data: [35, 15, 20, 20, 10],
            backgroundColor: [
              "#ff7a00", // نارنجی
              "#e74c3c", // قرمز
              "#3498db", // آبی
              "#f1c40f", // زرد
              "#1e1e1e", // خاکستری تم
            ],
            borderWidth: 0, // حذف حاشیه سفید پیش‌فرض برای زیبایی در تم تاریک
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "70%", // ضخامت حلقه
        plugins: {
          legend: { position: "bottom" },
        },
      },
    });
  }
});
