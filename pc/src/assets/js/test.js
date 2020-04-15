class Test {
  constructor() {

  }
  start(elem = '#outside-content') {
    let ele = document.querySelector(elem)
    ele.style.position = 'relative';

    let loadingBg = document.createElement('div')
    loadingBg.setAttribute('class', 'loading-bg')

    let loading = document.createElement('span')
    loading.setAttribute('class', 'loading-default')

    loadingBg.appendChild(loading)
    ele.appendChild(loadingBg)
  }
  close(elem = '#outside-content') {
    let str = elem + ' .loading-bg'
    let ele1 = document.querySelector(elem)
    let ele2 = document.querySelector(str)
    ele1.removeChild(ele2)
  }
}

export default new Test()