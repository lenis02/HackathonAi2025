async function loadResults() {
  try {
    const response = await fetch("/results");
    const data = await response.json();

    // 시간(ts)과 예측값(ac_power) 배열 추출
    const labels = data.map((r) => new Date(r.ts).toLocaleString());
    const values = data.map((r) => r.ac_power);

    // Chart.js로 그래프 그리기
    const ctx = document.getElementById("resultChart").getContext("2d");
    new Chart(ctx, {
      type: "line",
      data: {
        labels: labels.reverse(), // 오래된 것부터 보이도록
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

loadResults();
