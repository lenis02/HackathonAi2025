// // ================================================================
// // ✨ 최종 수정된 script.js (2025-08-21)
// // ================================================================

// document.addEventListener("DOMContentLoaded", function () {
//   // 현재 페이지가 main.html인지 확인
//   if (document.getElementById("goResultBtn")) {
//     // main.html의 '결과 확인' 버튼에 이벤트 연결
//     document
//       .getElementById("goResultBtn")
//       .addEventListener("click", goToResultPage);
//   }

//   // 현재 페이지가 result.html인지 확인
//   if (document.getElementById("resultChart")) {
//     // 결과 페이지 로직 초기화
//     initializeResultPage();
//   }
// });

// const plantMapping = {
//   "광주광역시 북구 용봉동": "4135001",
//   "전라북도 남원시 주천면 용담리": "4236001",
// };

// // --- main.html 용 함수 ---

// function goToResultPage() {
//   const region = document.getElementById("region")?.value;
//   const selectedPlantId = plantMapping[region];

//   if (!selectedPlantId) {
//     alert("지역을 먼저 선택하세요!");
//     return;
//   }

//   // 선택한 발전소 ID를 브라우저 임시 저장소에 저장
//   sessionStorage.setItem("selectedPlantId", selectedPlantId);

//   // 결과 페이지로 이동
//   window.location.href = "/result";
// }

// // --- result.html 용 함수 ---

// function initializeResultPage() {
//   const plantId = sessionStorage.getItem("selectedPlantId");
//   if (!plantId) {
//     alert("선택된 지역 정보가 없습니다. 메인 페이지로 돌아갑니다.");
//     window.location.href = "/";
//     return;
//   }

//   // 날짜 선택(flatpickr) 라이브러리 설정
//   const datePicker = flatpickr("#resultDateRange", {
//     dateFormat: "Y-m-d",
//     defaultDate: "today",
//     // ✅ 날짜가 변경될 때마다 차트를 다시 그리는 함수를 호출
//     onChange: function (selectedDates, dateStr, instance) {
//       fetchAndDrawChart(plantId, dateStr);
//     },
//   });

//   // 페이지 최초 로드 시, 오늘 날짜로 차트 그리기
//   fetchAndDrawChart(plantId, new Date().toISOString().split("T")[0]);
// }

// async function fetchAndDrawChart(plantId, date) {
//   const url = `/get_predictions?plant_id=${plantId}&date=${date}`;
//   console.log("API 요청:", url);

//   try {
//     const response = await fetch(url);
//     if (!response.ok) throw new Error("데이터 로딩 실패");

//     const data = await response.json();

//     // 결과 데이터 표시
//     document.getElementById("resultDate").innerText = data.requested_date;
//     document.getElementById("totalYield").innerText =
//       data.predicted_yield_for_requested_date.toFixed(2) + " kWh";

//     // 기존 차트가 있으면 파괴하고 새로 그림 (업데이트를 위해)
//     if (window.myChart) {
//       window.myChart.destroy();
//     }

//     const ctx = document.getElementById("resultChart").getContext("2d");
//     window.myChart = new Chart(ctx, {
//       type: "line",
//       data: {
//         labels: data.chart_data.map((r) => r.date),
//         datasets: [
//           {
//             label: "일별 예측 발전량 (Daily Yield)",
//             data: data.chart_data.map((r) => r.yield),
//             borderColor: "#4A90E2",
//             backgroundColor: "rgba(74, 144, 226, 0.1)",
//             fill: true,
//             tension: 0.3,
//           },
//         ],
//       },
//     });
//   } catch (err) {
//     console.error("차트 업데이트 실패:", err);
//     alert("결과를 불러오는 중 오류가 발생했습니다.");
//   }
// }

// ================================================================
// ✨ 최종 개선된 script.js (2025-08-21)
// ================================================================

document.addEventListener("DOMContentLoaded", function () {
  // 현재 페이지가 main.html일 경우, 버튼 이벤트 연결
  const goResultBtn = document.getElementById("goResultBtn");
  if (goResultBtn) {
    goResultBtn.addEventListener("click", goToResultPage);
  }

  // 현재 페이지가 result.html일 경우, 결과 페이지 초기화 함수 실행
  const resultChart = document.getElementById("resultChart");
  if (resultChart) {
    initializeResultPage();
  }
});

const plantMapping = {
  "광주광역시 북구 용봉동": "4135001",
  "전라북도 남원시 주천면 용담리": "4236001",
};

// --- main.html 용 함수 ---

function goToResultPage() {
  const region = document.getElementById("region")?.value;
  const selectedPlantId = plantMapping[region];

  if (!selectedPlantId) {
    alert("지역을 먼저 선택하세요!");
    return;
  }

  // 선택한 발전소 ID를 브라우저 임시 저장소에 저장
  sessionStorage.setItem("selectedPlantId", selectedPlantId);
  // 결과 페이지로 이동
  window.location.href = "/result";
}

// --- result.html 용 함수 ---

function initializeResultPage() {
  // ✅ 개선점: 차트 인스턴스를 함수 내 지역 변수로 관리하여 안정성 확보
  let chartInstance = null;

  const plantId = sessionStorage.getItem("selectedPlantId");
  if (!plantId) {
    alert("선택된 지역 정보가 없습니다. 메인 페이지로 돌아갑니다.");
    window.location.href = "/";
    return;
  }

  // 날짜 선택(flatpickr) 라이브러리 설정
  const datePicker = flatpickr("#resultDateRange", {
    defaultDate: "today", // 기본 선택 날짜는 오늘

    // ✅ 개선점: 달력이 처음 준비되었을 때 '한 번만' 실행되어 최초 차트를 그림
    onReady: function (selectedDates, dateStr, instance) {
      // flatpickr의 input 요소에서 직접 날짜 값을 가져와서 호출
      fetchAndDrawChart(instance.input.value);
    },

    // ✅ 개선점: 사용자가 날짜를 선택하고 달력을 '닫았을 때' 실행 (불필요한 호출 방지)
    onClose: function (selectedDates, dateStr, instance) {
      fetchAndDrawChart(dateStr);
    },
  });

  /**
   * API를 호출하고 차트를 그리는 핵심 함수
   * @param {string} date - 'YYYY-MM-DD' 형식의 날짜 문자열
   */
  async function fetchAndDrawChart(date) {
    if (!date) return; // 날짜가 없으면 실행 중단

    const url = `/get_predictions?plant_id=${plantId}&date=${date}`;
    console.log("API 요청:", url);

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error("데이터 로딩 실패");

      const data = await response.json();

      // 결과 데이터 표시
      document.getElementById("resultDate").innerText = data.requested_date;
      document.getElementById("totalYield").innerText =
        data.predicted_yield_for_requested_date.toFixed(2) + " kWh";

      // 기존 차트가 있으면 파괴
      if (chartInstance) {
        chartInstance.destroy();
      }

      // 새 차트를 생성하고 지역 변수에 저장
      const ctx = document.getElementById("resultChart").getContext("2d");
      chartInstance = new Chart(ctx, {
        type: "line",
        data: {
          labels: data.chart_data.map((r) => r.date),
          datasets: [
            {
              label: "일별 예측 발전량 (Daily Yield)",
              data: data.chart_data.map((r) => r.yield),
              borderColor: "#4A90E2",
              backgroundColor: "rgba(74, 144, 226, 0.1)",
              fill: true,
              tension: 0.3,
            },
          ],
        },
      });
    } catch (err) {
      console.error("차트 업데이트 실패:", err);
      // 사용자에게 더 친절한 에러 메시지 표시
      const chartContainer =
        document.getElementById("resultChart").parentElement;
      chartContainer.innerHTML = `<p style="color: red; text-align: center;">데이터를 불러오는 중 오류가 발생했습니다. (${date})</p>`;
    }
  }
}
