// 페이지가 로드된 후 실행
document.addEventListener("DOMContentLoaded", function () {
  flatpickr("#dateRange", {
    mode: "range", // 시작일과 종료일 선택
    dateFormat: "Y-m-d", // 날짜 포맷
    inline: true, // 상시 달력 표시
  });
});

// 저장 버튼 클릭 시
function saveDate() {
  const dateRange = document.getElementById("dateRange").value;
  if (!dateRange) {
    alert("날짜를 선택해 주세요!");
    return;
  }

  console.log("선택한 기간:", dateRange);

  // 예시: 백엔드로 보내는 fetch
  fetch("/save-date", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ dateRange: dateRange }),
  })
    .then((res) => res.json())
    .then((data) => alert("저장 완료: " + JSON.stringify(data)))
    .catch((err) => console.error(err));
}

async function goResult() {
  const payload = {
    plant_id: "test_plant", // 실제 입력값으로 교체 가능
    source_key: "test_source",
    ts: new Date().toISOString(),
    features: {
      AMBIENT_TEMPERATURE: 28.5,
      MODULE_TEMPERATURE: 42.7,
      IRRADIATION: 600.2,
    },
  };

  try {
    // 1. 로딩 화면 표시
    document.body.innerHTML = `
            <div style="display:flex;justify-content:center;align-items:center;height:100vh;flex-direction:column;">
                <h2>예측 중입니다... 잠시만 기다려주세요 ⏳</h2>
                <div class="spinner"></div>
            </div>
        `;

    // 2. /predict 요청
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) throw new Error("예측 요청 실패");

    // 3. 완료되면 /result 페이지로 이동
    window.location.href = "/result";
  } catch (err) {
    console.error("에러 발생:", err);
    alert("예측 요청 중 오류가 발생했습니다.");
  }
}
