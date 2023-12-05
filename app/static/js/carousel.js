class Carousel {
  constructor({
    // Array of images
    images,
    // Array of radio checkboxes
    radioButtons,
    // Auto slide timer interval
    interval,
    // Carousel element itself
    carousel,
    text
  }) {
    this.carousel = document.getElementById(carousel);
    this.images = [];
    for (let index = 0; index < images.length; index++) {
        this.images.push(document.getElementById(images[index]))
    }

    this.text = [];
    for (let index = 0; index < text.length; index++) {
      this.text.push(document.getElementById(text[index]))
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
    this.interval = interval;

    // Create event listener to start automatic slides once user scrolls into view
    this.scrollListener = (event) => {
      if (this.isInView()) {
        this.autoSlide();
        window.removeEventListener("scroll", this.scrollListener);
      }
    }
    addEventListener("scroll", this.scrollListener);

  }

  isInView() {
    var rect = this.carousel.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  }

  changeSlide(targetIndex) {

    // Set slide translateX to show target slide
    this.images.forEach((image, index) => {
      image.style.transform = `translateX(${(index - targetIndex) * 100}%)`;
    })
    // Change slide text
    this.text.forEach((text, index) => {
      if (index != targetIndex) {
        text.classList.add("carousel-text-hidden");
      }
      else {
        text.classList.remove("carousel-text-hidden");
      }
    })
    // Update curret position
    this.currentSlide = targetIndex;
  }

  autoSlide() {

    const autoSlideInterval = setInterval(() => {
      // Increment the currentSlide index to move to the next slide
      this.currentSlide++;

      // If currentSlide exceeds the maximum slide index, reset it to 0
      if (this.currentSlide >= this.maxSlide) {
        this.currentSlide = 0;
      }

      this.radioButtons[this.currentSlide].checked = true;

      // Call changeSlide method to show the next slide
      this.changeSlide(this.currentSlide);
    }, this.interval);

    // Clear the interval when the carousel is interacted with
    this.radioButtons.forEach((radio) => {
      radio.addEventListener("change", () => {
        clearInterval(autoSlideInterval);
      });
    });
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
  interval: 5000,
  carousel: "carousel",
  text: [
    "carousel-text-1",
    "carousel-text-2",
    "carousel-text-3",
  ]
})
