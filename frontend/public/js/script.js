const plantMapping = {
  "광주광역시 북구 용봉동": "4135001",
  "전라북도 남원시 주천면 용담리": "4236001",
};

let selectedPlantId = null;

// 페이지가 로드된 후 실행
document.addEventListener("DOMContentLoaded", function () {
  flatpickr("#dateRange", {
    dateFormat: "Y-m-d",
    mode: "single", // <- 여기서 하루만 선택 가능
    defaultDate: new Date(),
  });
});

// 지역 저장
function saveRegion() {
  const region = document.getElementById("region")?.value;
  if (!region || !plantMapping[region]) {
    alert("지역을 선택하세요!");
    return;
  } else {
    alert("지역이 입력되었습니다");
  }
  selectedPlantId = plantMapping[region];

  //   // 백엔드로 전송
  //   fetch("/save-region", {
  //     method: "POST",
  //     headers: { "Content-Type": "application/json" },
  //     body: JSON.stringify({ city, district, dong, zipcode }),
  //   })
  //     .then((res) => res.json())
  //     .then((data) => alert("지역 저장 완료: " + JSON.stringify(data)))
  //     .catch((err) => console.error(err));
}

// 기간 저장 (하루만 선택 가능)
// function saveDate() {
//   const dateRange = document.getElementById("dateRange").value;
//   if (!dateRange) {
//     alert("날짜를 선택해 주세요!");
//     return;
//   }

//   console.log("선택한 기간:", dateRange);

//   // 시작일, 종료일 분리
//   const dates = dateRange.split(" to ");
//   if (dates.length !== 2) {
//     alert("기간을 올바르게 선택해 주세요!");
//     return;
//   }

//   const start = new Date(dates[0]);
//   const end = new Date(dates[1]);

//   // 날짜 차이 (일 단위)
//   const diffDays = (end - start) / (1000 * 60 * 60 * 24);

//   if (diffDays !== 0) {
//     // 하루만 허용
//     alert("기간은 하루만 선택 가능합니다!");
//     return;
//   }

//   console.log("선택한 날짜:", start);

//   // 예시: 백엔드로 보내는 fetch
//   fetch("/save-date", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ date: start.toISOString().split("T")[0] }),
//   })
//     .then((res) => res.json())
//     .then((data) => alert("저장 완료: " + JSON.stringify(data)))
//     .catch((err) => console.error(err));
// }

async function goResult() {
  if (!selectedPlantId) {
    alert("지역을 먼저 선택하세요!");
    return;
  }

  const loading = document.getElementById("loading");
  if (loading) loading.style.display = "block";

  const requestBody = {
    plant_id: selectedPlantId,
    source_key: "TEMP_KEY",
    ts: new Date().toISOString(),
    features: {
      AMBIENT_TEMPERATURE: 25.0,
      MODULE_TEMPERATURE: 35.0,
      IRRADIATION: 500.0,
    },
  };

  try {
    await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });

    // 예측 완료 → 결과 페이지로 이동
    window.location.href = "/result";
  } catch (err) {
    console.error("예측 요청 실패:", err);
  }
}

// async function goResult() {
//   const payload = {
//     plant_id: "test_plant", // 실제 입력값으로 교체 가능
//     source_key: "test_source",
//     ts: new Date().toISOString(),
//     features: {
//       AMBIENT_TEMPERATURE: 28.5,
//       MODULE_TEMPERATURE: 42.7,
//       IRRADIATION: 600.2,
//     },
//   };

//   try {
//     // 1. 로딩 화면 표시
//     document.body.innerHTML = `
//             <div style="display:flex;justify-content:center;align-items:center;height:100vh;flex-direction:column;">
//                 <h2>예측 중입니다... 잠시만 기다려주세요 ⏳</h2>
//                 <div class="spinner"></div>
//             </div>
//         `;

//     // 2. /predict 요청
//     const response = await fetch("/predict", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify(payload),
//     });

//     if (!response.ok) throw new Error("예측 요청 실패");

//     // 3. 완료되면 /result 페이지로 이동

//     window.location.href = "/result";
//   } catch (error) {
//     alert("오류가 발생했습니다: " + error.message);
//   } finally {
//     // (옵션) result.html로 이동 후엔 로딩창 자동으로 사라짐
//     document.getElementById("loading").style.display = "none";
//   }
// }

function initResultPage() {
  if (document.getElementById("dateRange")) {
    flatpickr("#dateRange", { mode: "range" });
    loadResults(); // 기본 조회
  }
}

async function loadResults() {
  try {
    const response = await fetch("/results");
    const data = await response.json();

    // 날짜 필터링
    const dateRange = document.getElementById("dateRange").value.split(" to ");
    let filtered = data;
    if (dateRange.length === 2) {
      const start = new Date(dateRange[0]);
      const end = new Date(dateRange[1]);
      filtered = data.filter((r) => {
        const ts = new Date(r.ts);
        return ts >= start && ts <= end;
      });
    }

    const labels = filtered.map((r) => new Date(r.ts).toLocaleString());
    const values = filtered.map((r) => r.ac_power);

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
    });
  } catch (err) {
    console.error("결과 조회 실패:", err);
  }
}

window.addEventListener("DOMContentLoaded", initResultPage);
