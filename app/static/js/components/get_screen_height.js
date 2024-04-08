// Get device screen height and set stylesheet property var
const appHeight = () => {
    const doc = document.documentElement;
    //  Subtract height of navbar
    const height = window.innerHeight - 54;
    doc.style.setProperty('--app-height', `${height}px`)
}

// Add event listen to update var on screen resize
window.addEventListener('resize', appHeight)
appHeight()
