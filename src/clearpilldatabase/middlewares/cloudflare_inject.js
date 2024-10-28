console.log('inject')
console.clear = () => console.log('Console was cleared')
var opts = {};
const i = setInterval(() => {
    if (window.turnstile) {
        console.log('turns')
        clearInterval(i)
        window.turnstile.render = (a, b) => {
            console.log('renderd')
            let params = {
                sitekey: b.sitekey,
                data: b.cData,
                pagedata: b.chlPageData,
                action: b.action,
                json: 1
            }
            console.log('after parms')
            console.log('intercepted-params:' + JSON.stringify(params))
            window.cfCallback = b.callback
            return
        }
    }
}, 50)