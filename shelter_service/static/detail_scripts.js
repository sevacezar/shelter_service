document.addEventListener('DOMContentLoaded', function() {
  const mainImage = document.querySelector('.main-image');
  const thumbnails = document.querySelectorAll('.thumbnail');
  const prevButton = document.querySelector('.prev-button');
  const nextButton = document.querySelector('.next-button');

  let allImages = [mainImage.src, ...Array.from(thumbnails).map(thumb => thumb.src)];
  let currentImageIndex = 0;

  function updateMainImage(newIndex) {
    if (newIndex < 0) newIndex = allImages.length - 1;
    if (newIndex >= allImages.length) newIndex = 0;

    currentImageIndex = newIndex;

    mainImage.animate([
      { opacity: 0.5 },
      { opacity: 1 }
    ], {
      duration: 300,
      easing: 'ease-in-out'
    });

    mainImage.src = allImages[currentImageIndex];

    thumbnails.forEach((thumbnail, idx) => {
      let thumbIndex = (currentImageIndex + idx + 1) % allImages.length;
      thumbnail.src = allImages[thumbIndex];
    });
  }

  prevButton.addEventListener('click', () => {
    updateMainImage(currentImageIndex - 1);
  });

  nextButton.addEventListener('click', () => {
    updateMainImage(currentImageIndex + 1);
  });

  thumbnails.forEach((thumbnail, index) => {
    thumbnail.addEventListener('click', function() {
      const clickedIndex = index + 1;
      updateMainImage(clickedIndex);
    });
  });

  const adoptionButton = document.querySelector('.adoption-button');
  adoptionButton.addEventListener('click', function() {
    alert('Спасибо за интерес к Барону! Мы свяжемся с вами для обсуждения деталей усыновления.');
  });
});
