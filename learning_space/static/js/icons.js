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
            align-items: center;
            justify-content: center;
            margin-right: 2px;
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
          align-items: center;
          justify-content: center;
          margin-right: 2px;
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

class IconStarEmpty extends HTMLElement {
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
          align-items: center;
          justify-content: center;
          margin-right: 2px;
        }
        svg {
          width: 13px;
          color: var(--theme-color-1);
        }
    </style>
    <svg viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
      <path fill="currentColor" d="M1024 397.056l-353.792-51.392L512 25.088 353.792 345.664 0 397.056l256 249.536-60.416 352.32L512 832.576l316.416 166.336L768 646.592l256-249.536z m-512 356.416l-223.488 117.504 42.688-248.832L150.4 445.952l249.856-36.288L512 183.296l111.744 226.368 249.856 36.288-180.8 176.192 42.688 248.832L512 753.472z"></path>
    </svg>
    `;
  }
}

class IconClose extends HTMLElement {
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
        align-items: center;
        justify-content: center;
      }
      svg {
        width: 100%;
        color: var(--theme-color-1);
      }
    </style>
    <svg viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
      <path fill="currentColor" d="M512 128C300.8 128 128 300.8 128 512s172.8 384 384 384 384-172.8 384-384S723.2 128 512 128zM512 832c-179.2 0-320-140.8-320-320s140.8-320 320-320 320 140.8 320 320S691.2 832 512 832z"></path>
      <path fill="currentColor" d="M672 352c-12.8-12.8-32-12.8-44.8 0L512 467.2 396.8 352C384 339.2 364.8 339.2 352 352S339.2 384 352 396.8L467.2 512 352 627.2c-12.8 12.8-12.8 32 0 44.8s32 12.8 44.8 0L512 556.8l115.2 115.2c12.8 12.8 32 12.8 44.8 0s12.8-32 0-44.8L556.8 512l115.2-115.2C684.8 384 684.8 364.8 672 352z"></path>
    </svg>
    `;
  }
}

customElements.define('icon-star', IconStar);
customElements.define('icon-star-half', IconStarHalf);
customElements.define('icon-star-empty', IconStarEmpty);
customElements.define('icon-close', IconClose);