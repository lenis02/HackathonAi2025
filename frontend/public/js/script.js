// 페이지가 로드된 후 실행
document.addEventListener("DOMContentLoaded", function() {
    flatpickr("#dateRange", {
        mode: "range",       // 시작일과 종료일 선택
        dateFormat: "Y-m-d", // 날짜 포맷
        inline: true         // 상시 달력 표시
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
        body: JSON.stringify({ dateRange: dateRange })
    })
    .then(res => res.json())
    .then(data => alert("저장 완료: " + JSON.stringify(data)))
    .catch(err => console.error(err));
}


function goResult() {
    window.location.href = "result.html"; // result.html로 이동
}