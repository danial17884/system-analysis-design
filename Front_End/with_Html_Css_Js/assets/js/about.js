// about.js (اختیاری)
document.addEventListener("DOMContentLoaded", () => {
  const teamCards = document.querySelectorAll(".team-card");

  // یک افکت ساده برای نمایش کارت‌ها با تاخیر
  teamCards.forEach((card, index) => {
    card.style.opacity = "0";
    card.style.transform = "translateY(20px)";
    card.style.transition = "all 0.5s ease";

    setTimeout(() => {
      card.style.opacity = "1";
      card.style.transform = "translateY(0)";
    }, 150 * index); // هر کارت ۱۵۰ میلی‌ثانیه بعد از کارت قبلی ظاهر می‌شود
  });
});
