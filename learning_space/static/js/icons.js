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
            width: 20px;
            color: green;
          }
        </style>
        <svg viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
          <path fill="currentColor" d="M731.428571 18.285714l0 765.147429-256.585143 134.875429q-12.580571 6.875429-22.820571 6.875429-11.995429 0-17.993143-8.265143t-5.997714-20.260571q0-3.437714 1.170286-11.410286l49.152-285.696-208.018286-202.313143q-14.262857-15.433143-14.262857-27.428571 0-21.138286 32.036571-26.258286l286.866286-41.691429 128.585143-260.022857q10.825143-23.405714 28.013714-23.405714z"></path>
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
        width: 20px;
        color: green;
        }
    </style>
    <svg viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
        <path fill="currentColor" d="M908.1 353.1l-253.9-36.9L540.7 86.1c-3.1-6.3-8.2-11.4-14.5-14.5-15.8-7.8-35-1.3-42.9 14.5L369.8 316.2l-253.9 36.9c-7 1-13.4 4.3-18.3 9.3-12.3 12.7-12.1 32.9 0.6 45.3l183.7 179.1-43.4 252.9c-1.2 6.9-0.1 14.1 3.2 20.3 8.2 15.6 27.6 21.7 43.2 13.4L512 754l227.1 119.4c6.2 3.3 13.4 4.4 20.3 3.2 17.4-3 29.1-19.5 26.1-36.9l-43.4-252.9 183.7-179.1c5-4.9 8.3-11.3 9.3-18.3 2.7-17.5-9.5-33.7-27-36.3z"></path>
    </svg>
    `;
  }
}

customElements.define('icon-star', IconStar);
customElements.define('icon-star-half', IconStarHalf);