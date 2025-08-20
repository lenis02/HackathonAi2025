const data = {
        "광주광역시": {
          "북구": { "용봉동": "61186", "운암동": "61187" },
          "서구": { "치평동": "62250", "농성동": "62251" }
        },
        "서울특별시": {
          "강남구": { "역삼동": "06220", "삼성동": "06174" },
          "서초구": { "반포동": "06590", "서초동": "06600" }
        }
      };

      function updateDistricts() {
        const city = document.getElementById('city').value;
        const districtSelect = document.getElementById('district');
        const dongSelect = document.getElementById('dong');
        const zipcodeInput = document.getElementById('zipcode');

        districtSelect.innerHTML = '<option value="">선택</option>';
        dongSelect.innerHTML = '<option value="">선택</option>';
        zipcodeInput.value = '';

        if(city && data[city]) {
          Object.keys(data[city]).forEach(d => {
            const option = document.createElement('option');
            option.value = d;
            option.text = d;
            districtSelect.appendChild(option);
          });
        }
      }

      function updateDongs() {
        const city = document.getElementById('city').value;
        const district = document.getElementById('district').value;
        const dongSelect = document.getElementById('dong');
        const zipcodeInput = document.getElementById('zipcode');

        dongSelect.innerHTML = '<option value="">선택</option>';
        zipcodeInput.value = '';

        if(city && district && data[city][district]) {
          Object.keys(data[city][district]).forEach(dong => {
            const option = document.createElement('option');
            option.value = dong;
            option.text = dong;
            dongSelect.appendChild(option);
          });
        }
      }

      function updateZipcode() {
        const city = document.getElementById('city').value;
        const district = document.getElementById('district').value;
        const dong = document.getElementById('dong').value;
        const zipcodeInput = document.getElementById('zipcode');

        if(city && district && dong && data[city][district][dong]) {
          zipcodeInput.value = data[city][district][dong];
        } else {
          zipcodeInput.value = '';
        }
      }

      function saveRegion() {
        const city = document.getElementById('city').value;
        const district = document.getElementById('district').value;
        const dong = document.getElementById('dong').value;
        const zipcode = document.getElementById('zipcode').value;

        if(!city || !district || !dong) {
          alert('모든 지역을 선택해주세요.');
          return;
        }

        alert(`선택된 지역: ${city} ${district} ${dong} (${zipcode})`);
      }