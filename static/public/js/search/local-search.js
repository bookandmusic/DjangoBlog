window.addEventListener('load', () => {
    let loadFlag = false
    const openSearch = function () {
        document.body.style.cssText = 'width: 100%;overflow: hidden'
        document.querySelector('#local-search .search-dialog').style.display = 'block'
        document.querySelector('#local-search-input input').focus()
    }

    const closeSearch = function () {
        document.body.style.cssText = "width: '';overflow: ''"
        const $searchDialog = document.querySelector('#local-search .search-dialog')
        $searchDialog.style.animation = 'search_close .5s'
        setTimeout(() => {
            $searchDialog.style.cssText = "display: none; animation: ''"
        }, 500)
        btf.fadeOut(document.getElementById('search-mask'), 0.5)
    }

    // click function
    const searchClickFn = () => {
        document.querySelector('#search-button > .search').addEventListener('click', openSearch)
        document.getElementById('search-mask').addEventListener('click', closeSearch)
        document.querySelector('#local-search .search-close-button').addEventListener('click', closeSearch)
    }

    searchClickFn()
})
