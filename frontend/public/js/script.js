// 페이지가 로드된 후 실행
document.addEventListener("DOMContentLoaded", function() {
    flatpickr("#dateRange", {
    dateFormat: "Y-m-d",
    mode: "single", // <- 여기서 하루만 선택 가능
    defaultDate: new Date(),
    });
});

// 지역 저장 
function saveRegion() {
    const city = document.getElementById("city").value;
    const district = document.getElementById("district").value;
    const dong = document.getElementById("dong").value;
    const zipcode = document.getElementById("zipcode").value;

    // 유효성 검사
    if (!city || !district || !dong) {
        alert("도시, 군/구, 동을 모두 선택해 주세요!");
        return;
    }

    console.log("선택한 지역:", { city, district, dong, zipcode });

    // 백엔드로 전송
    fetch("/save-region", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ city, district, dong, zipcode })
    })
    .then(res => res.json())
    .then(data => alert("지역 저장 완료: " + JSON.stringify(data)))
    .catch(err => console.error(err));
}


// 기간 저장 (하루만 선택 가능)
function saveDate() {
    const dateRange = document.getElementById("dateRange").value;

    if (!dateRange) {
        alert("날짜를 선택해 주세요!");
        return;
    }

    console.log("선택한 기간:", dateRange);

    // 시작일, 종료일 분리
    const dates = dateRange.split(" to ");
    if (dates.length !== 2) {
        alert("기간을 올바르게 선택해 주세요!");
        return;
    }

    const start = new Date(dates[0]);
    const end = new Date(dates[1]);

    // 날짜 차이 (일 단위)
    const diffDays = (end - start) / (1000 * 60 * 60 * 24);

    if (diffDays !== 0) { // 하루만 허용
        alert("기간은 하루만 선택 가능합니다!");
        return;
    }

    console.log("선택한 날짜:", start);

    // 예시: 백엔드로 보내는 fetch
    fetch("/save-date", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ date: start.toISOString().split("T")[0] })
    })
    .then(res => res.json())
    .then(data => alert("저장 완료: " + JSON.stringify(data)))
    .catch(err => console.error(err));
}


// function goResult() {
//     window.location.href = "result.html"; // result.html로 이동
// }

async function goResult() {
  // 스피너 표시
  document.getElementById("loading").style.display = "block";

  try {
    // 입력값을 JSON으로 묶어서 전달 (예시)
    const payload = {
      city: document.getElementById("city")?.value,
      district: document.getElementById("district")?.value,
      startDate: document.getElementById("startDate")?.value,
      endDate: document.getElementById("endDate")?.value
    };

    // /predict API 요청
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!response.ok) throw new Error("예측 요청 실패");

    // 결과 페이지로 이동
    window.location.href = "result.html";
  } catch (error) {
    alert("오류가 발생했습니다: " + error.message);
  } finally {
    // (옵션) result.html로 이동 후엔 로딩창 자동으로 사라짐
    document.getElementById("loading").style.display = "none";
  }
}