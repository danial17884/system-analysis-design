// transactions.js

// داده‌های تستی (در پروژه واقعی از API دریافت می‌شود)
let transactions = [
  {
    id: 1,
    title: "خرید اشتراک سرور",
    amount: 500000,
    type: "expense",
    date: "1405/03/05",
  },
  {
    id: 2,
    title: "واریز حقوق",
    amount: 15000000,
    type: "income",
    date: "1405/03/01",
  },
  {
    id: 3,
    title: "خرید قهوه",
    amount: 80000,
    type: "expense",
    date: "1405/03/06",
  },
];

document.addEventListener("DOMContentLoaded", () => {
  const tableBody = document.querySelector("#transactions-table tbody");
  const transactionForm = document.querySelector("#add-transaction-form");
  const filterSelect = document.querySelector("#filter-type");

  // تابع رندر کردن جدول تراکنش‌ها
  function renderTable(data) {
    if (!tableBody) return;
    tableBody.innerHTML = ""; // پاک کردن جدول

    data.forEach((trx) => {
      const row = document.createElement("tr");
      // استایل‌دهی بر اساس نوع تراکنش (سبز برای درآمد، قرمز/نارنجی برای هزینه)
      const amountClass =
        trx.type === "income" ? "text-success" : "text-danger";
      const amountSign = trx.type === "income" ? "+" : "-";

      row.innerHTML = `
                <td>${trx.title}</td>
                <td class="${amountClass}" dir="ltr">${amountSign} ${trx.amount.toLocaleString()} تومان</td>
                <td>${trx.date}</td>
                <td>
                    <span class="badge ${trx.type === "income" ? "bg-success" : "bg-orange"}">
                        ${trx.type === "income" ? "درآمد" : "هزینه"}
                    </span>
                </td>
                <td>
                    <button class="btn-delete" onclick="deleteTransaction(${trx.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
      tableBody.appendChild(row);
    });
  }

  // افزودن تراکنش جدید
  if (transactionForm) {
    transactionForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const title = document.querySelector("#trx-title").value;
      const amount = parseInt(document.querySelector("#trx-amount").value);
      const type = document.querySelector("#trx-type").value;

      const newTrx = {
        id: Date.now(),
        title: title,
        amount: amount,
        type: type,
        date: new Date().toLocaleDateString("fa-IR"), // تاریخ امروز شمسی
      };

      transactions.push(newTrx);
      renderTable(transactions);
      transactionForm.reset();
    });
  }

  // فیلتر کردن تراکنش‌ها
  if (filterSelect) {
    filterSelect.addEventListener("change", (e) => {
      const filterValue = e.target.value;
      if (filterValue === "all") {
        renderTable(transactions);
      } else {
        const filtered = transactions.filter((t) => t.type === filterValue);
        renderTable(filtered);
      }
    });
  }

  // رندر اولیه
  renderTable(transactions);
});

// تابع حذف تراکنش (در سطح گلوبال تعریف شده تا در onclick کار کند)
window.deleteTransaction = function (id) {
  if (confirm("آیا از حذف این تراکنش مطمئن هستید؟")) {
    transactions = transactions.filter((t) => t.id !== id);
    // فراخوانی مجدد رندر با استفاده از یک رویداد کاستوم یا انتخاب مستقیم
    document.querySelector("#filter-type").dispatchEvent(new Event("change"));
  }
};
