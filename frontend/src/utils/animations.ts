import gsap from 'gsap'

export const slideUp = (element: HTMLElement, delay = 0) => {
  return gsap.from(element, {
    y: 50,
    opacity: 0,
    duration: 0.8,
    delay,
    ease: 'power2.out'
  })
}

export const fadeIn = (element: HTMLElement, delay = 0) => {
  return gsap.from(element, {
    opacity: 0,
    duration: 0.6,
    delay,
    ease: 'power1.out'
  })
}

export const staggerChildren = (parent: HTMLElement, selector: string, stagger = 0.1) => {
  const elements = parent.querySelectorAll(selector)
  return gsap.from(elements, {
    y: 20,
    opacity: 0,
    duration: 0.6,
    stagger,
    ease: 'power2.out'
  })
}

export const cosmic = {
  sparkle: (element: HTMLElement) => {
    gsap.to(element, {
      keyframes: [
        { scale: 1, opacity: 1, duration: 0.1 },
        { scale: 1.2, opacity: 0.8, duration: 0.2 },
        { scale: 1, opacity: 1, duration: 0.1 }
      ],
      ease: 'none'
    })
  },

  pulse: (element: HTMLElement) => {
    return gsap.to(element, {
      scale: 1.05,
      duration: 1,
      repeat: -1,
      yoyo: true,
      ease: 'power1.inOut'
    })
  },

  orbit: (element: HTMLElement, radius = 20) => {
    const duration = 2 + Math.random() * 2
    const delay = Math.random() * 2

    return gsap.to(element, {
      keyframes: [
        { x: radius, y: 0 },
        { x: 0, y: radius },
        { x: -radius, y: 0 },
        { x: 0, y: -radius },
        { x: radius, y: 0 }
      ],
      duration,
      delay,
      ease: 'none',
      repeat: -1
    })
  }
}
