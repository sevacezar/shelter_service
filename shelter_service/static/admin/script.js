// Mock data for different entities with extended fields
const mockData = {
  users: [
    { 
      id: 1, 
      name: 'Анна Иванова', 
      email: 'anna@example.com', 
      role: 'Администратор', 
      registrationDate: '2023-01-15',
      phone: '+7 (999) 123-45-67',
      address: 'ул. Ленина, 42, кв. 56',
      lastLogin: '2023-06-15 14:30',
      status: 'Активен',
      notes: 'Опытный волонтер приюта',
      preferences: 'Работа с собаками',
      volunteerHours: '120'
    },
    { 
      id: 2, 
      name: 'Петр Сидоров', 
      email: 'petr@example.com', 
      role: 'Модератор', 
      registrationDate: '2023-02-20',
      phone: '+7 (999) 234-56-78',
      address: 'ул. Пушкина, 15, кв. 23',
      lastLogin: '2023-06-14 16:45',
      status: 'Активен',
      notes: 'Специалист по работе с кошками',
      preferences: 'Работа с кошками',
      volunteerHours: '85'
    },
    { 
      id: 3, 
      name: 'Мария Петрова', 
      email: 'maria@example.com', 
      role: 'Пользователь', 
      registrationDate: '2023-03-10',
      phone: '+7 (999) 345-67-89',
      address: 'ул. Гагарина, 78, кв. 12',
      lastLogin: '2023-06-13 10:15',
      status: 'Неактивен',
      notes: 'Новый волонтер',
      preferences: 'Административная работа',
      volunteerHours: '25'
    }
  ],
  pets: [
    { 
      id: 1, 
      name: 'Барон', 
      species: 'Собака', 
      breed: 'Немецкая овчарка', 
      age: 2, 
      status: 'Доступен',
      weight: '32 кг',
      color: 'Черно-коричневый',
      gender: 'Мужской',
      sterilized: 'Да',
      vaccinated: 'Да',
      healthStatus: 'Здоров',
      arrivalDate: '2023-01-10',
      personality: 'Дружелюбный, активный',
      specialNeeds: 'Нет',
      dietaryRequirements: 'Стандартный корм',
      photos: [
        {
          id: 1,
          url: 'https://images.unsplash.com/photo-1589941013453-ec89f33b5e95?w=300',
          description: 'Барон в парке',
          isAvatar: true
        },
        {
          id: 2, 
          url: 'https://images.unsplash.com/photo-1586671267731-da2cf3ceeb80?w=300',
          description: 'Играет с мячом',
          isAvatar: false
        },
        {
          id: 3,
          url: 'https://images.unsplash.com/photo-1576201836106-db1758fd1c97?w=300',
          description: 'Отдыхает на диване',
          isAvatar: false
        },
        {
          id: 4,
          url: 'https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=300',
          description: 'На прогулке',
          isAvatar: false
        }
      ]
    },
    { 
      id: 2, 
      name: 'Мурка', 
      species: 'Кошка', 
      breed: 'Сиамская', 
      age: 1, 
      status: 'На передержке',
      weight: '3.5 кг',
      color: 'Кремовый с темными пятнами',
      gender: 'Женский',
      sterilized: 'Да',
      vaccinated: 'Да',
      healthStatus: 'Здорова',
      arrivalDate: '2023-02-15',
      personality: 'Ласковая, спокойная',
      specialNeeds: 'Гипоаллергенный корм',
      dietaryRequirements: 'Специальная диета',
      photos: [
        {
          id: 1,
          url: 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=300',
          description: 'Мурка на подоконнике',
          isAvatar: true
        },
        {
          id: 2,
          url: 'https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=300',
          description: 'Играет с игрушкой',
          isAvatar: false
        },
        {
          id: 3,
          url: 'https://images.unsplash.com/photo-1495360010541-f48722b34f7d?w=300',
          description: 'Спит в корзинке',
          isAvatar: false
        },
        {
          id: 4,
          url: 'https://images.unsplash.com/photo-1561948955-570b270e7c36?w=300',
          description: 'В домике',
          isAvatar: false
        }
      ]
    },
    { 
      id: 3, 
      name: 'Рекс', 
      species: 'Собака', 
      breed: 'Лабрадор', 
      age: 3, 
      status: 'Усыновлен',
      weight: '28 кг',
      color: 'Золотистый',
      gender: 'Мужской',
      sterilized: 'Да',
      vaccinated: 'Да',
      healthStatus: 'Здоров',
      arrivalDate: '2023-03-20',
      personality: 'Энергичный, любит детей',
      specialNeeds: 'Необходимы регулярные физические нагрузки',
      dietaryRequirements: 'Стандартный корм',
      photos: []
    }
  ],
  views: [
    { 
      id: 1, 
      petName: 'Барон', 
      userName: 'Анна Иванова', 
      date: '2023-06-01', 
      duration: '15 мин',
      purpose: 'Первичное знакомство',
      outcome: 'Позитивное взаимодействие',
      staffNotes: 'Хороший контакт с животным',
      followUpNeeded: 'Да',
      scheduledNextVisit: '2023-06-08',
      interactionDetails: 'Животное проявило дружелюбие',
      recommendations: 'Рекомендуется повторный визит'
    },
    { 
      id: 2, 
      petName: 'Мурка', 
      userName: 'Петр Сидоров', 
      date: '2023-06-02', 
      duration: '20 мин',
      purpose: 'Последующее знакомство',
      outcome: 'Нейтральное взаимодействие',
      staffNotes: 'Животное проявляет интерес',
      followUpNeeded: 'Нет',
      scheduledNextVisit: '2023-06-12',
      interactionDetails: 'Животное проявляет активность',
      recommendations: 'Рекомендуется наблюдение'
    },
    { 
      id: 3, 
      petName: 'Рекс', 
      userName: 'Мария Петрова', 
      date: '2023-06-03', 
      duration: '10 мин',
      purpose: 'Первичное знакомство',
      outcome: 'Позитивное взаимодействие',
      staffNotes: 'Хороший контакт с животным',
      followUpNeeded: 'Да',
      scheduledNextVisit: '2023-06-09',
      interactionDetails: 'Животное проявило дружелюбие',
      recommendations: 'Рекомендуется повторный визит'
    }
  ],
  adoptions: [
    { 
      id: 1, 
      petName: 'Барон', 
      applicant: 'Иван Петров', 
      status: 'На рассмотрении', 
      date: '2023-06-01',
      homeCheckStatus: 'Запланирован',
      previousPetExperience: 'Есть опыт содержания собак',
      homeType: 'Частный дом',
      familyMembers: '4 человека',
      otherPets: 'Нет',
      veterinarianContact: 'Др. Иванов',
      incomeVerification: 'Подтверждено',
      adoptionAgreement: 'Не подписано',
      followUpDates: '2023-07-01, 2023-08-01'
    },
    { 
      id: 2, 
      petName: 'Мурка', 
      applicant: 'Елена Сидорова', 
      status: 'Одобрено', 
      date: '2023-06-02',
      homeCheckStatus: 'Проведен',
      previousPetExperience: 'Нет опыта',
      homeType: 'Квартира',
      familyMembers: '2 человека',
      otherPets: 'Нет',
      veterinarianContact: 'Др. Петрова',
      incomeVerification: 'Подтверждено',
      adoptionAgreement: 'Подписано',
      followUpDates: '2023-07-05, 2023-08-05'
    },
    { 
      id: 3, 
      petName: 'Рекс', 
      applicant: 'Алексей Иванов', 
      status: 'Завершено', 
      date: '2023-06-03',
      homeCheckStatus: 'Проведен',
      previousPetExperience: 'Есть опыт содержания собак',
      homeType: 'Частный дом',
      familyMembers: '3 человека',
      otherPets: 'Есть кошка',
      veterinarianContact: 'Др. Иванов',
      incomeVerification: 'Подтверждено',
      adoptionAgreement: 'Подписано',
      followUpDates: '2023-07-10, 2023-08-10'
    }
  ]
};

// Table column configurations for different entities (showing only main fields)
const tableConfigs = {
  users: ['ID', 'Имя', 'Email', 'Роль', 'Дата регистрации'],
  pets: ['ID', 'Имя', 'Вид', 'Порода', 'Возраст', 'Статус'],
  views: ['ID', 'Питомец', 'Посетитель', 'Дата', 'Длительность'],
  adoptions: ['ID', 'Питомец', 'Заявитель', 'Статус', 'Дата']
};

// Main fields to show in table (rest will be shown in modals)
const mainFields = {
  users: ['id', 'name', 'email', 'role', 'registrationDate'],
  pets: ['id', 'name', 'species', 'breed', 'age', 'status'],
  views: ['id', 'petName', 'userName', 'date', 'duration'],
  adoptions: ['id', 'petName', 'applicant', 'status', 'date']
};

// Define readonly fields
const readOnlyFields = {
  users: ['registrationDate', 'lastLogin'],
  pets: ['arrivalDate'],
  views: ['date'],
  adoptions: ['date']
};

function showToast(message) {
  // Create toast element
  const toast = document.createElement('div');
  toast.className = 'toast success';
  toast.innerHTML = `
    <i class="fas fa-check-circle"></i>
    <span>${message}</span>
  `;
  
  document.body.appendChild(toast);
  
  // Show toast
  setTimeout(() => {
    toast.classList.add('active');
  }, 100);
  
  // Hide and remove toast after 3 seconds
  setTimeout(() => {
    toast.classList.remove('active');
    setTimeout(() => {
      document.body.removeChild(toast);
    }, 300);
  }, 3000);
}

document.addEventListener('DOMContentLoaded', () => {
  const entityLinks = document.querySelectorAll('.entity-link');
  const contentTitle = document.querySelector('.content-header h1');
  const tableBody = document.getElementById('tableBody');
  const searchInput = document.getElementById('searchInput');
  const deleteModal = document.getElementById('deleteModal');
  const viewModal = document.getElementById('viewModal');
  const editModal = document.getElementById('editModal');
  const cancelDelete = document.getElementById('cancelDelete');
  const confirmDelete = document.getElementById('confirmDelete');
  const closeView = document.getElementById('closeView');
  const closeEdit = document.getElementById('closeEdit');
  const saveEdit = document.getElementById('saveEdit');
  const viewContent = document.getElementById('viewContent');
  const editContent = document.getElementById('editContent');
  const addModal = document.getElementById('addModal');
  const closeAdd = document.getElementById('closeAdd');
  const confirmAdd = document.getElementById('confirmAdd');
  const addButton = document.querySelector('.add-button');
  
  let currentEntity = 'users';
  let itemToDelete = null;
  let currentItem = null;

  function filterData(entity, searchQuery) {
    if (!searchQuery.trim()) {
      return mockData[entity];
    }
    
    const query = searchQuery.toLowerCase();
    return mockData[entity].filter(item => {
      // Search through all string and number values in the item
      return Object.values(item).some(value => {
        if (typeof value === 'string' || typeof value === 'number') {
          return String(value).toLowerCase().includes(query);
        }
        return false;
      });
    });
  }

  function generateFormContent(item = null, isEditable = false, isNew = false) {
    let formContent = '<div class="form-grid">';
    
    if (isNew) {
      // Generate empty form for new item
      const templateItem = {};
      // Create template based on first item in current entity
      const entityTemplate = mockData[currentEntity][0];
      Object.keys(entityTemplate).forEach(key => {
        if (key !== 'id' && key !== 'photos') {
          templateItem[key] = '';
        }
      });
      
      if (currentEntity === 'pets') {
        templateItem.photos = [];
        Object.entries(templateItem)
          .filter(([key]) => key !== 'id' && key !== 'photos')
          .forEach(([key, value]) => {
            const isLongField = key === 'notes' || key === 'description' || key === 'address';
            const isReadOnly = readOnlyFields[currentEntity]?.includes(key);
            formContent += generateFormField(key, value, true, isLongField, isReadOnly);
          });
        formContent += '</div>';
        formContent += generatePhotoSection([], true);
      } else {
        Object.entries(templateItem)
          .filter(([key]) => key !== 'id')
          .forEach(([key, value]) => {
            const isLongField = key === 'notes' || key === 'description' || key === 'address';
            const isReadOnly = readOnlyFields[currentEntity]?.includes(key);
            formContent += generateFormField(key, value, true, isLongField, isReadOnly);
          });
        formContent += '</div>';
      }
    } else if (item) {
      // Handle photos separately for pets
      if (currentEntity === 'pets') {
        const photoSection = generatePhotoSection(item.photos, isEditable);
        Object.entries(item)
          .filter(([key]) => key !== 'id' && key !== 'photos')
          .forEach(([key, value]) => {
            const isLongField = key === 'notes' || key === 'description' || key === 'address';
            const isReadOnly = readOnlyFields[currentEntity]?.includes(key);
            
            formContent += generateFormField(key, value, isEditable, isLongField, isReadOnly);
          });
        formContent += '</div>';
        formContent += photoSection;
      } else {
        // Original logic for other entities
        Object.entries(item)
          .filter(([key]) => key !== 'id')
          .forEach(([key, value]) => {
            const isLongField = key === 'notes' || key === 'description' || key === 'address';
            const isReadOnly = readOnlyFields[currentEntity]?.includes(key);
            
            formContent += generateFormField(key, value, isEditable, isLongField, isReadOnly);
          });
        formContent += '</div>';
      }
    }
    
    return formContent;
  }

  function generateFormField(key, value, isEditable, isLongField, isReadOnly) {
    return `
      <div class="form-group ${isLongField ? 'full-width' : ''}">
        <label>${key.charAt(0).toUpperCase() + key.slice(1)}:</label>
        ${isEditable 
          ? isReadOnly
            ? `<input type="text" name="${key}" value="${value}" class="form-control readonly" readonly>`
            : `<input type="text" name="${key}" value="${value}" class="form-control">`
          : `<p class="form-control-static">${value}</p>`
        }
      </div>
    `;
  }

  function generatePhotoSection(photos, isEditable) {
    let photoContent = `
      <div class="photos-section">
        <h3>Фотографии</h3>
        <div class="photos-grid">
    `;
    
    photos.forEach(photo => {
      if (isEditable) {
        photoContent += `
          <div class="photo-item" data-photo-id="${photo.id}">
            <img src="${photo.url}" alt="${photo.description}">
            <div class="photo-controls">
              <input type="text" class="photo-description" value="${photo.description}" placeholder="Описание">
              <label class="avatar-checkbox">
                <input type="checkbox" ${photo.isAvatar ? 'checked' : ''} onchange="handleAvatarChange(${photo.id})">
                Аватар
              </label>
              <button type="button" class="delete-photo-btn" onclick="deletePhoto(${photo.id})">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
        `;
      } else {
        photoContent += `
          <div class="photo-item">
            <img src="${photo.url}" alt="${photo.description}" onclick="showLargePhoto('${photo.url}')">
            <div class="photo-info">
              <p>${photo.description}</p>
              ${photo.isAvatar ? '<span class="avatar-badge">Аватар</span>' : ''}
            </div>
          </div>
        `;
      }
    });
    
    if (isEditable) {
      photoContent += `
        <div class="add-photo-item">
          <input type="file" id="newPhotoInput" accept="image/*" style="display: none">
          <button type="button" onclick="document.getElementById('newPhotoInput').click()" class="add-photo-btn">
            <i class="fas fa-plus"></i>
            Добавить фото
          </button>
        </div>
      `;
    }
    
    photoContent += `
        </div>
      </div>
    `;
    
    return photoContent;
  }

  window.showLargePhoto = function(url) {
    const modal = document.createElement('div');
    modal.className = 'photo-modal';
    modal.innerHTML = `
      <div class="large-photo-container">
        <img src="${url.replace('w=300', 'w=800')}" alt="Увеличенное фото">
        <button class="close-photo-modal" onclick="this.parentElement.parentElement.remove()">
          <i class="fas fa-times"></i>
        </button>
      </div>
    `;
    
    document.body.appendChild(modal);
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.remove();
      }
    });
  };

  window.deletePhoto = function(photoId) {
    if (currentItem && currentItem.photos) {
      currentItem.photos = currentItem.photos.filter(p => p.id !== photoId);
      editContent.innerHTML = generateFormContent(currentItem, true);
      showToast('Фото успешно удалено');
    }
  };

  window.handleAvatarChange = function(photoId) {
    if (currentItem && currentItem.photos) {
      // Uncheck all other avatar checkboxes
      currentItem.photos.forEach(photo => {
        photo.isAvatar = (photo.id === photoId);
      });
      // Refresh the photo section
      editContent.innerHTML = generateFormContent(currentItem, true);
      showToast('Аватар успешно обновлен');
    }
  };

  document.body.addEventListener('change', (e) => {
    if (e.target.matches('#newPhotoInput')) {
      e.preventDefault(); // Prevent form submission
      const file = e.target.files[0];
      if (file) {
        // Simulate file upload
        const reader = new FileReader();
        reader.onload = (e) => {
          if (!currentItem.photos) {
            currentItem.photos = [];
          }
          const newPhoto = {
            id: currentItem.photos.length ? Math.max(...currentItem.photos.map(p => p.id)) + 1 : 1,
            url: 'https://images.unsplash.com/photo-1576201836106-db1758fd1c97?w=300', // placeholder URL
            description: 'Новое фото',
            isAvatar: currentItem.photos.length === 0 // Make first photo avatar by default
          };
          
          currentItem.photos.push(newPhoto);
          editContent.innerHTML = generateFormContent(currentItem, true);
          showToast('Фото успешно добавлено');
        };
        reader.readAsDataURL(file);
      }
    }
  });

  function updateTable(entity, searchQuery = '') {
    const data = filterData(entity, searchQuery);
    tableBody.innerHTML = '';
    
    // Update table headers
    const headerRow = document.querySelector('.data-table thead tr');
    headerRow.innerHTML = '';
    tableConfigs[entity].forEach(header => {
      const th = document.createElement('th');
      th.textContent = header;
      headerRow.appendChild(th);
    });
    // Add actions header
    const actionsHeader = document.createElement('th');
    actionsHeader.textContent = 'Действия';
    headerRow.appendChild(actionsHeader);
    
    // Update table body
    data.forEach(item => {
      const tr = document.createElement('tr');
      mainFields[entity].forEach(field => {
        const td = document.createElement('td');
        td.textContent = item[field];
        tr.appendChild(td);
      });

      // Add actions column
      const actionsTd = document.createElement('td');
      actionsTd.innerHTML = `
        <div class="action-buttons">
          <button class="action-button view" title="Просмотр">
            <i class="fas fa-eye"></i>
          </button>
          <button class="action-button edit" title="Редактировать">
            <i class="fas fa-edit"></i>
          </button>
          <button class="action-button delete" title="Удалить">
            <i class="fas fa-trash"></i>
          </button>
        </div>
      `;

      // Action button handlers
      const viewBtn = actionsTd.querySelector('.view');
      const editBtn = actionsTd.querySelector('.edit');
      const deleteBtn = actionsTd.querySelector('.delete');

      viewBtn.addEventListener('click', () => {
        currentItem = item;
        viewContent.innerHTML = generateFormContent(item);
        viewModal.classList.add('active');
      });

      editBtn.addEventListener('click', () => {
        currentItem = item;
        editContent.innerHTML = generateFormContent(item, true);
        editModal.classList.add('active');
      });

      deleteBtn.addEventListener('click', () => {
        itemToDelete = item.id;
        deleteModal.classList.add('active');
      });

      tr.appendChild(actionsTd);
      tableBody.appendChild(tr);
    });
  }

  const modals = document.querySelectorAll('.modal');

  modals.forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeAllModals();
      }
    });
  });

  function closeAllModals() {
    modals.forEach(modal => {
      modal.classList.remove('active');
    });
    itemToDelete = null;
    currentItem = null;
  }

  // Initialize with users data
  updateTable(currentEntity);

  // Add search input handler
  searchInput.addEventListener('input', (e) => {
    updateTable(currentEntity, e.target.value);
  });

  // Entity navigation
  entityLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      entityLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');
      
      currentEntity = link.dataset.entity;
      contentTitle.textContent = link.textContent.trim();
      // Clear search input when switching entities
      searchInput.value = '';
      updateTable(currentEntity);
    });
  });

  // Modal handlers
  cancelDelete.addEventListener('click', closeAllModals);

  confirmDelete.addEventListener('click', () => {
    if (itemToDelete) {
      mockData[currentEntity] = mockData[currentEntity].filter(item => item.id !== itemToDelete);
      updateTable(currentEntity);
      closeAllModals();
      showToast('Запись успешно удалена');
    }
  });

  closeView.addEventListener('click', closeAllModals);
  closeEdit.addEventListener('click', closeAllModals);

  saveEdit.addEventListener('click', () => {
    if (currentItem) {
      const formData = new FormData(document.getElementById('editForm'));
      const updatedData = {};
      formData.forEach((value, key) => {
        updatedData[key] = value;
      });
      
      const index = mockData[currentEntity].findIndex(item => item.id === currentItem.id);
      if (index !== -1) {
        mockData[currentEntity][index] = { 
          id: currentItem.id,
          ...updatedData
        };
        updateTable(currentEntity);
      }
      
      closeAllModals();
      showToast('Изменения успешно сохранены');
    }
  });

  addButton.addEventListener('click', () => {
    document.getElementById('addContent').innerHTML = generateFormContent(null, true, true);
    addModal.classList.add('active');
  });

  closeAdd.addEventListener('click', closeAllModals);
  
  confirmAdd.addEventListener('click', addNewItem);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeAllModals();
    }
  });

  function addNewItem() {
    const formData = new FormData(document.getElementById('addForm'));
    const newData = {};
    formData.forEach((value, key) => {
      newData[key] = value;
    });
    
    // Add additional fields for pets
    if (currentEntity === 'pets') {
      newData.photos = []; // Initialize empty photos array for new pet
    }
    
    const maxId = Math.max(...mockData[currentEntity].map(item => item.id));
    newData.id = maxId + 1;
    
    mockData[currentEntity].push(newData);
    updateTable(currentEntity);
    closeAllModals();
    showToast('Запись успешно добавлена');
  }
});