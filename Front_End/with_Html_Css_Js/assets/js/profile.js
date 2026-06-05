// profile.js

document.addEventListener("DOMContentLoaded", () => {
  // ۱. پیش‌نمایش تغییر عکس پروفایل
  const avatarInput = document.getElementById("avatar-upload");
  const avatarPreview = document.getElementById("avatar-preview");

  if (avatarInput && avatarPreview) {
    avatarInput.addEventListener("change", function () {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          avatarPreview.src = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // ۲. مدیریت فرم بروزرسانی اطلاعات
  const profileForm = document.getElementById("profile-form");
  if (profileForm) {
    profileForm.addEventListener("submit", (e) => {
      e.preventDefault();

      // گرفتن مقادیر فرم
      const name = document.getElementById("user-name").value;
      const email = document.getElementById("user-email").value;

      // شبیه‌سازی ارسال به سرور
      const submitBtn = profileForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;

      submitBtn.innerHTML =
        '<i class="fas fa-spinner fa-spin"></i> در حال ذخیره...';
      submitBtn.disabled = true;

      setTimeout(() => {
        // نمایش پیام موفقیت (در پروژه واقعی از کتابخانه‌هایی مثل Toastify یا SweetAlert استفاده می‌شود)
        alert(`اطلاعات با موفقیت بروزرسانی شد!\nنام: ${name}`);

        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
      }, 1500); // تاخیر مصنوعی ۱.۵ ثانیه‌ای
    });
  }

  // ۳. اعتبارسنجی فرم تغییر رمز عبور
  const passwordForm = document.getElementById("password-form");
  if (passwordForm) {
    passwordForm.addEventListener("submit", (e) => {
      e.preventDefault();

      const newPass = document.getElementById("new-password").value;
      const confirmPass = document.getElementById("confirm-password").value;

      if (newPass !== confirmPass) {
        alert("رمز عبور جدید و تکرار آن با هم مطابقت ندارند!");
        return;
      }

      if (newPass.length < 8) {
        alert("رمز عبور باید حداقل ۸ کاراکتر باشد.");
        return;
      }

      alert("رمز عبور شما با موفقیت تغییر کرد.");
      passwordForm.reset();
    });
  }
});
