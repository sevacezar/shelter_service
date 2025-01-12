function updateDropdownText(container) {
  const selectedOptions = [...container.querySelectorAll('input:checked')].map(
    input => input.parentElement.textContent.trim()
  );
  const displayText = container.querySelector('.selected-options');
  if (selectedOptions.length === 0) {
    displayText.textContent = `Select ${container.dataset.filter}...`;
  } else {
    displayText.textContent = selectedOptions.join(', ');
  }
}

document.querySelectorAll('.dropdown-container').forEach(container => {
  const header = container.querySelector('.dropdown-header');
  const options = container.querySelector('.dropdown-options');

  // Открытие-закрытие выпадающешго списка
  header.addEventListener('click', () => {
    options.classList.toggle('show');
  });

  // Обновление текста выбранных элементов
  container.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', () => {
      updateDropdownText(container);
      applyFilters();
    });
  });

  // Закрытие списка при клике вне области
  document.addEventListener('click', e => {
    if (!container.contains(e.target)) {
      options.classList.remove('show');
    }
  });
});