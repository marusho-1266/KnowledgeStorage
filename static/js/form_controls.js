document.addEventListener('DOMContentLoaded', function() {
    // エリアと部署の連動選択の設定
    const areaRadios = document.querySelectorAll('.area-radio');
    const departmentOptions = document.getElementById('department-options');
    
    if (areaRadios.length > 0 && departmentOptions) {
        // エリアラジオボタン変更時のイベントリスナー
        areaRadios.forEach(function(radio) {
            radio.addEventListener('change', function() {
                if (this.checked) {
                    updateDepartments(this.value);
                }
            });
        });
        
        // 初期ロード時に選択されているエリアの部署を設定
        const selectedArea = document.querySelector('.area-radio:checked');
        if (selectedArea) {
            updateDepartments(selectedArea.value);
        } else if (areaRadios.length > 0) {
            // デフォルトで最初のエリアを選択（新規追加時）
            areaRadios[0].checked = true;
            updateDepartments(areaRadios[0].value);
        }
    }
    
    // エリア選択に基づいて部署のオプションを更新
    function updateDepartments(selectedArea) {
        const departmentsData = JSON.parse(document.getElementById('departments-data').getAttribute('data-departments'));
        
        // 部署エリアをクリア
        departmentOptions.innerHTML = '';
        
        // 選択されたエリアに対応する部署リストを取得
        const departments = departmentsData[selectedArea] || [];
        
        // 既存の部署値（編集時）
        const currentDepartment = document.getElementById('current-department')?.value || '';
        
        // 部署がない場合のメッセージ
        if (departments.length === 0) {
            const emptyMsg = document.createElement('div');
            emptyMsg.className = 'col-12';
            emptyMsg.textContent = '選択されたエリアには部署がありません。';
            departmentOptions.appendChild(emptyMsg);
            return;
        }
        
        // 部署のラジオボタンを追加
        departments.forEach(function(department, index) {
            const colDiv = document.createElement('div');
            colDiv.className = 'col-md-4 mb-2';
            
            const formCheck = document.createElement('div');
            formCheck.className = 'form-check';
            
            const input = document.createElement('input');
            input.className = 'form-check-input';
            input.type = 'radio';
            input.name = 'department';
            input.id = 'department_' + index;
            input.value = department;
            input.required = true;
            
            // 編集時に現在の値を選択、または最初の値を選択
            if (department === currentDepartment) {
                input.checked = true;
            } else if (index === 0 && currentDepartment === '') {
                input.checked = true;
            }
            
            const label = document.createElement('label');
            label.className = 'form-check-label';
            label.setAttribute('for', 'department_' + index);
            label.textContent = department;
            
            formCheck.appendChild(input);
            formCheck.appendChild(label);
            colDiv.appendChild(formCheck);
            departmentOptions.appendChild(colDiv);
        });
    }
}); 