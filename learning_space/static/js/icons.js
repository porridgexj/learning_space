class IconStarHalf extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.render();
  }
  render() {
    this.shadowRoot.innerHTML = `
        <style>
          :host {
            display: flex;
          }
          svg {
            width: 13px;
            color: var(--theme-color-1);
            zoom: 99%;
          }
        </style>
        <svg viewBox="0 0 1072 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
          <path fill="currentColor" d="M1017.1089 343.02L724.3689 300.4 593.5489 35.62C581.7889 11.96 558.8489 0 535.9089 0c-22.8 0-45.58 11.8-57.38 35.62l-130.86 264.76-292.76 42.58c-52.5 7.6-73.54 72.18-35.48 109.18l211.78 206-50.12 290.96C173.9689 990.66 207.1489 1024 244.3089 1024c9.86 0 20-2.34 29.74-7.5l261.9-137.36 261.88 137.4c9.72 5.1 19.84 7.42 29.66 7.42 37.2 0 70.44-33.22 63.32-74.8l-50.06-290.98 211.82-205.96c38.08-37 17.04-101.6-35.46-109.2z m-243.48 246.4l-36.24 35.24 8.56 49.76 39.04 226.9-204.26-107.18-44.76-23.48 0.06-634.38 102.06 206.58 22.36 45.26 50.02 7.28 228.46 33.26-165.3 160.76z"></path>
        </svg>
      `;
  }
}

class IconStar extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.render();
  }
  render() {
    this.shadowRoot.innerHTML = `
    <style>
        :host {
          display: flex;
        }
        svg {
          width: 12px;
          color: var(--theme-color-1);
        }
    </style>
    <svg viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
      <path fill="currentColor" d="M565.273 34.627L677.369 272.17c8.706 18.32 25.411 31.051 44.823 33.996l250.776 38.081c48.698 7.411 68.225 70.046 32.934 105.98L824.407 635.164c-13.998 14.23-20.352 34.815-17.059 54.935l42.82 261.127c8.346 50.696-42.643 89.452-86.226 65.519L539.634 893.474c-17.286-9.526-37.992-9.526-55.278 0l-224.314 123.27c-43.583 23.934-94.572-14.822-86.22-65.518L216.638 690.1c3.32-20.12-3.089-40.705-17.087-54.935L18.11 450.227c-35.285-35.934-15.818-98.574 32.934-105.98l250.75-38.081c19.35-2.94 36.082-15.675 44.756-33.996L458.673 34.627c21.825-46.168 84.836-46.168 106.6 0z"></path>
    </svg>
    `;
  }
}

customElements.define('icon-star', IconStar);
customElements.define('icon-star-half', IconStarHalf);