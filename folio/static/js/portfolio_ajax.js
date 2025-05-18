document.addEventListener('DOMContentLoaded', function () {
    const csrfToken = document.querySelector('[data-csrf]').dataset.csrf;

    // Сохранение количества ajax
    document.querySelectorAll('.btn-save').forEach(button => {
        button.addEventListener('click', function () {
            const row = this.closest('tr');
            const secid = row.dataset.securityId;
            const quantityInput = row.querySelector('.quantity-input');
            const quantity = parseInt(quantityInput.value);

            if (isNaN(quantity) || quantity < 0) {
                alert("Введите корректное количество");
                return;
            }

            const folioId = document.querySelector('[data-folio-id]').dataset.folioId;

            fetch(`/folios/${folioId}/update_quantity/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ security_id: secid, quantity: quantity })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (quantity === 0) {
                        row.remove();
                    }
                    window.location.reload();
                } else {
                    alert('Ошибка: ' + (data.error || 'Не удалось сохранить'));
                }
            });
        });
    });

    // Удаление ajax
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function () {
            const row = this.closest('tr');
            const secid = row.dataset.securityId;

            if (!confirm("Вы уверены, что хотите удалить эту запись?")) return;

            const folioId = document.querySelector('[data-folio-id]').dataset.folioId;

            fetch(`/folios/${folioId}/delete/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ security_id: secid })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    row.remove();
                    window.location.reload();
                } else {
                    alert('Ошибка при удалении');
                }
            });
        });
    });
});