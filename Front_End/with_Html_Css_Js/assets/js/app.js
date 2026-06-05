// app.js (برای استفاده مشترک در صفحات پنل)

document.addEventListener("DOMContentLoaded", () => {
  // ۱. مدیریت خروج از حساب (Logout) مشترک در کل سیستم
  const logoutBtn = document.querySelector(".logout");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", (e) => {
      e.preventDefault(); // جلوگیری از رفتار پیش‌فرض لینک

      const confirmLogout = confirm(
        "آیا مطمئن هستید که می‌خواهید از حساب کاربری خارج شوید؟",
      );
      if (confirmLogout) {
        // پاک کردن کش یا توکن در سیستم واقعی
        window.location.href = "login.html";
      }
    });
  }

  // ۲. مدیریت منوی موبایل (ریسپانسیو کردن سایدبار)
  // نکته: در HTML باید یک دکمه با آی‌دی mobile-menu-btn برای هدر موبایل اضافه کنید
  const mobileMenuBtn = document.getElementById("mobile-menu-btn");
  const sidebar = document.querySelector(".sidebar");
  const menuItems = document.querySelector(".menu");

  if (mobileMenuBtn && sidebar && menuItems) {
    mobileMenuBtn.addEventListener("click", () => {
      // تغییر وضعیت نمایش منو در سایز موبایل
      menuItems.classList.toggle("show-mobile-menu");

      // در صورتی که نیاز به تغییر آیکن همبرگری به ضربدر داشتید:
      const icon = mobileMenuBtn.querySelector("i");
      if (icon) {
        icon.classList.toggle("fa-bars");
        icon.classList.toggle("fa-times");
      }
    });
  }

  // ۳. نمایش تاریخ شمسی امروز در هدر (اختیاری برای زیبایی پروژه)
  const dateDisplay = document.getElementById("current-date");
  if (dateDisplay) {
    const options = {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    };
    dateDisplay.textContent = new Date().toLocaleDateString("fa-IR", options);
  }
});
