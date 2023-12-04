class Carousel {
  constructor({
    // Array of images
    images,
    // Array of radio checkboxes
    radioButtons,
    // Index of initial starting checked radio input
    initPos,
  }) {
    this.images = [];
    for (let index = 0; index < images.length; index++) {
        this.images.push(document.getElementById(images[index]))
    }

    this.radioButtons = [];
    for (let index = 0; index < radioButtons.length; index++) {
        this.radioButtons.push(document.getElementById(radioButtons[index]))
    }
    
    this.radioButtons.forEach(radio => {
      radio.addEventListener("change", (event) => {
        if (event.target.checked) {
          // Set carousel target position to selected value
          this.targetPos = event.target.value;
          this.changeSlide(this.targetPos);
        }
      });

      // Set each slide transformX to index * 100%
      this.images.forEach((image, index) => {
        image.style.transform = `translateX(${index * 100}%)`;
      })
    });

    this.currentSlide = 0;
    this.maxSlide = this.images.length;
  }

  changeSlide(targetIndex) {

    // Set slide translateX to show target slide
    this.images.forEach((image, index) => {
      image.style.transform = `translateX(${(index - targetIndex) * 100}%)`;
    })

    // Update curret position
    this.currentSlide = this.targetPos;
  }

}


const carousel = new Carousel({
  images: [
    "carousel-img-1",
    "carousel-img-2",
    "carousel-img-3"
  ],
  radioButtons: [
    "carousel-button-1",
    "carousel-button-2",
    "carousel-button-3",
  ],
  initPos: 0
})
