// 📅 flatpickr: 하루만 선택 가능
flatpickr("#datePicker", {
  dateFormat: "Y-m-d", // YYYY-MM-DD 형식
  mode: "single",
  defaultDate: new Date(),
});

async function loadResults() {
  try {
    const date = document.getElementById("datePicker").value;

    // 날짜 파라미터 추가 (백엔드 /results?date=YYYY-MM-DD)
    const response = await fetch(`/results?date=${date}`);
    const data = await response.json();

    // 시간(ts)과 예측값(ac_power) 배열 추출
    const labels = data.map((r) => new Date(r.ts).toLocaleString());
    const values = data.map((r) => r.ac_power);

    // Chart.js로 그래프 그리기
    const ctx = document.getElementById("resultChart").getContext("2d");
    new Chart(ctx, {
      type: "line",
      data: {
        labels: labels.reverse(),
        datasets: [
          {
            label: "예측 발전량 (AC_POWER)",
            data: values.reverse(),
            borderColor: "blue",
            backgroundColor: "rgba(0, 0, 255, 0.1)",
            fill: true,
            tension: 0.3,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "top" },
        },
        scales: {
          x: { title: { display: true, text: "시간" } },
          y: { title: { display: true, text: "발전량 (W)" } },
        },
      },
    });
  } catch (err) {
    console.error("결과 조회 실패:", err);
  }
}
