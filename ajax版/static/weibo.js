// TODO API
// 获取所有 weibo
var apiWeiboAll = function(callback) {
    var path = '/api/weibo/all'
    ajax('GET', path, '', callback)
}


var apiCommentDelete = function(id ,callback) {
    var path = `/api/comment/delete?id=${id}`
    ajax('GET', path, '', callback)
}



var apiCommentAll = function(callback) {
    var path = '/api/comment/all'
    ajax('GET', path, '', callback)
}

// 增加一个 weibo
var apiWeiboAdd = function(form, callback) {
    var path = '/api/weibo/add'
    ajax('POST', path, form, callback)
}


var apiCommentAdd = function(form, callback) {
    var path = '/api/comment/add'
    ajax('POST', path, form, callback)
}

var apiCommentUpdate = function(form, callback) {
    var path = '/api/comment/update'
    ajax('POST', path, form, callback)
}

var apiWeiboUpdate = function(form, callback) {
    var path = '/api/weibo/update'
    ajax('POST', path, form, callback)
}

var apiWeiboDelete = function(id,callback) {
    var path = `/api/weibo/delete?id=${id}`
    ajax('GET', path, '', callback)
}

// TODO DOM
var weiboTemplate = function(weibo) {
    var t = `
        <div class="weibo-cell" id = weibo${weibo.id}>
            <button data-id=${weibo.id} class="weibo-delete">删除</button>
            <button data-id=${weibo.id} class="weibo-edit">编辑</button>
            <span class= "weibo-content">${weibo.content}</span>
            <br>
            <span>评论</span>
            <br>
            <input id = 'id-input-comment'>
            <button data-id=${weibo.id} class="comment-add">添加评论</button>
        </div>

    `
//
//        <div class="comment-add" >
//            <input id='id-input-comment'>
//            <button id='id-comment-add'>添加评论</button>
//
//        </div>
    return t
}


var commentTemplate = function(comment) {
    var t = `
        <div class="comment-cell">
            <button data-id=${comment.id} class="comment-delete">删除</button>
            <button data-id=${comment.id} class="comment-edit">编辑</button>
            <span class= "comment-content">${comment.content}</span>
        </div>
    `
    return t
}


var weiboUpdateTemplate = function(weiboId) {
    var t = `
        <div class="weibo-update-form">
            <input class="weibo-update-input">
            <button data-id=${weiboId} class="weibo-update">更新</button>
        </div>
    `
    return t
}

var commentUpdateTemplate = function(comment_id) {
    var t = `
        <div class="comment-update-form">
            <input class = "comment-update-input">
            <button data-id=${comment_id} class="comment-update">更新</button>
        </div>
    `
    return t
}


var insertWeibo = function(weibo) {
    var weiboCell = weiboTemplate(weibo)
    // 插入 weibo-list
    var weiboList = e('.weibo-list')
    log('weibo-list',weiboList.dataset.id )
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}


var insertComment = function(comment) {
    var commentCell = commentTemplate(comment)
    var weiboId = comment.weibo_id
    //查找comment中对应的weibo_id
    log('weibo_id',weiboId)
    var weibo = e(`#weibo${weiboId}`)
    log('weibo',weibo)


    if (weibo == null){
        log('无评论')}
    else{
        var weibocell = weibo.closest('.weibocell')
        weibo.insertAdjacentHTML('beforeEnd', commentCell)}
//        edit_button.parentElement.insertAdjacentHTML('beforeend', editCell)
}


var insertUpdate = function(edit_button) {
    var weiboId = edit_button.dataset.id
    // 插入 weibo-list
    var editCell = weiboUpdateTemplate(weiboId)
    edit_button.parentElement.insertAdjacentHTML('beforeend', editCell)
}


var insertCommentUpdate = function(edit_button) {

    var commentId = edit_button.dataset.id
    var editCell = commentUpdateTemplate(commentId)
    // 插入 todo-list

    edit_button.parentElement.insertAdjacentHTML('beforeend', editCell)
}

var loadWeibos = function() {
    // 调用 ajax api 来载入数据
    apiWeiboAll(function(r) {
        console.log('load all', r)
        // 解析为 数组
        var weibos = JSON.parse(r)
        // 循环添加到页面中
        for(var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            insertWeibo(weibo)
        }
    })
}


var loadComments = function() {
    // 调用 ajax api 来载入数据
    apiCommentAll(function(r) {
        console.log('load all', r)
        // 解析为 数组
        var comments = JSON.parse(r)
        // 循环添加到页面中
        for(var i = 0; i < comments.length; i++) {
            var comment = comments[i]
            insertComment(comment)
        }
    })
}

var bindEventWeiboAdd = function() {
    var b = e('#id-button-add')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(){
        var input = e('#id-input-weibo')
        var content = input.value
        log('click add', content)
        var form = {
            content: content,
        }
        apiWeiboAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var weibo = JSON.parse(r)
            insertWeibo(weibo)
        })
    })
}


var bindEventCommentAdd = function(){
    var weiboList = e('.weibo-list')
    // 事件响应函数会被传入一个参数, 就是事件本身
    weiboList.addEventListener('click', function(event){

     // 我们可以通过 event.target 来得到被点击的元素
     var self = event.target

     // 判断是否拥有某个 class 的方法如下
     if (self.classList.contains('comment-add')) {
         log('点到了 添加评论按钮',self.dataset.id)
         var weiboCell = self.closest('.weibo-cell')
         var input = weiboCell.querySelector('#id-input-comment')
         var weiboId = self.dataset.id
         log('comment_weiboId',weiboId)
         var form = {
            weibo_id: weiboId,
            content: input.value,

         }
         log('form',form)
         apiCommentAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var comment = JSON.parse(r)
            insertComment(comment,self)
     })}
     else {
          log('点击的不是更新按钮******')
     }
 })}



var bindEventWeiboDelete = function(){
    var weiboList = e('.weibo-list')
    // 事件响应函数会被传入一个参数, 就是事件本身
    weiboList.addEventListener('click', function(event){
    // log('click weibolist', event)
    // 我们可以通过 event.target 来得到被点击的元素
    var self = event.target
    // log('被点击的元素是', self)
    // 通过比较被点击元素的 class 来判断元素是否是我们想要的
    // classList 属性保存了元素的所有 class
    // 在 HTML 中, 一个元素可以有多个 class, 用空格分开
    // log(self.classList)
    // 判断是否拥有某个 class 的方法如下
    if (self.classList.contains('weibo-delete')) {
        log('点到了 删除按钮',self.dataset.id)
        var weiboId = self.dataset.id
        // 删除 self 的父节点
        // parentElement 可以访问到元素的父节点

        apiWeiboDelete(weiboId,function(r) {
            self.parentElement.remove()
        })
     }
     else {
          log('点击的不是删除按钮******')
     }
 })
}


var bindEventCommentDelete = function() {
     var todoList = e('.weibo-list')
     // 事件响应函数会被传入一个参数, 就是事件本身
     todoList.addEventListener('click', function(event){

     var self = event.target

     if (self.classList.contains('comment-delete')) {
         log('点到了 删除按钮',self.dataset.id)
         var comment_id = self.dataset.id

         apiCommentDelete(comment_id,function(r){
            self.parentElement.remove()

         })

     } else {
          log('点击的不是删除按钮******')
     }
 })
 }


var bindEventWeiboEdit = function(){
    var weiboList = e('.weibo-list')
    // 事件响应函数会被传入一个参数, 就是事件本身
    weiboList.addEventListener('click', function(event){
    // log('click weibolist', event)
    // 我们可以通过 event.target 来得到被点击的元素
    var self = event.target
    // log('被点击的元素是', self)
    // 通过比较被点击元素的 class 来判断元素是否是我们想要的
    // classList 属性保存了元素的所有 class
    // 在 HTML 中, 一个元素可以有多个 class, 用空格分开
    // log(self.classList)
    // 判断是否拥有某个 class 的方法如下
    if (self.classList.contains('weibo-edit')) {
        log('点到了 编辑按钮',self.dataset.id)
        var weiboId = self.dataset.id
        //插入编辑输入框
        insertUpdate(self)
    } else {
          log('点击的不是吧编辑按钮******')
     }
 })

}


var bindEventCommentEdit = function(){
    var weiboList = e('.weibo-list')
    // 事件响应函数会被传入一个参数, 就是事件本身
    weiboList.addEventListener('click', function(event){
    var self = event.target
    if (self.classList.contains('comment-edit')) {
        log('点到了 编辑按钮',self.dataset.id)
        var commentId = self.dataset.id
        //插入编辑输入框
        insertCommentUpdate(self)
    } else {
         // log('点击的不是吧编辑按钮******')
     }
 })

}

var bindEventWeiboUpdate = function(){
    var weiboList = e('.weibo-list')
    // 事件响应函数会被传入一个参数, 就是事件本身
    weiboList.addEventListener('click', function(event){

    // 我们可以通过 event.target 来得到被点击的元素
    var self = event.target

    // 判断是否拥有某个 class 的方法如下
    if (self.classList.contains('weibo-update')) {
        log('点到了 更新按钮',self.dataset.id)
        var weiboCell = self.closest('.weibo-cell')
        var input = weiboCell.querySelector('.weibo-update-input')
        var weiboId = self.dataset.id

        var form = {
           id: weiboId,
           content: input.value,

        }
        apiWeiboUpdate(form,function(r){
           log('收到更新数据',r)

           var updateForm = weiboCell.querySelector('.weibo-update-form')
           updateForm.remove()

           var weibo = JSON.parse(r)
           var weiboTask = weiboCell.querySelector('.weibo-content')
           weiboTask.innerText = weibo.content
        })
    } else {
         // log('点击的不是更新按钮******')
    }
 })

}


var bindEventCommentUpdate = function(){
    var weiboList = e('.weibo-list')
    // 事件响应函数会被传入一个参数, 就是事件本身
    weiboList.addEventListener('click', function(event){

    // 我们可以通过 event.target 来得到被点击的元素
    var self = event.target

    // 判断是否拥有某个 class 的方法如下
    if (self.classList.contains('comment-update')) {
        log('点到了 更新按钮',self.dataset.id)
        var commentCell = self.closest('.comment-cell')
        var input = commentCell.querySelector('.comment-update-input')
        var commentId = self.dataset.id

        var form = {
           id: commentId,
           content: input.value,

        }
        log("form",form)
        apiCommentUpdate(form,function(r){
           log('收到更新数据',r)

           var updateForm = commentCell.querySelector('.comment-update-form')
           updateForm.remove()

           var comment = JSON.parse(r)
           var commentTask = commentCell.querySelector('.comment-content')
           commentTask.innerText = comment.content
        })
    } else {
         // log('点击的不是更新按钮******')
    }
 })

}


var bindEvents = function() {
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
    bindEventCommentAdd()
    bindEventCommentDelete()
    bindEventCommentEdit()
    bindEventCommentUpdate()

}

var __main = function() {
    bindEvents()
    loadWeibos()
    loadComments()
}

__main()






/*
给 删除 按钮绑定删除的事件
1, 绑定事件
2, 删除整个 weibo-cell 元素
*/
// var weiboList = e('.weibo-list')
// // 事件响应函数会被传入一个参数, 就是事件本身
// weiboList.addEventListener('click', function(event){
//     // log('click weibolist', event)
//     // 我们可以通过 event.target 来得到被点击的元素
//     var self = event.target
//     // log('被点击的元素是', self)
//     // 通过比较被点击元素的 class 来判断元素是否是我们想要的
//     // classList 属性保存了元素的所有 class
//     // 在 HTML 中, 一个元素可以有多个 class, 用空格分开
//     // log(self.classList)
//     // 判断是否拥有某个 class 的方法如下
//     if (self.classList.contains('weibo-delete')) {
//         log('点到了 删除按钮')
//         // 删除 self 的父节点
//         // parentElement 可以访问到元素的父节点
//         self.parentElement.remove()
//     } else {
//         // log('点击的不是删除按钮******')
//     }
// })
weibo.js
var apiWeiboAll = function(callback) {
    var path = '/api/weibo/all'
    ajax('GET', path, '', callback)
}

var apiCommentAll = function(callback) {
    var path = '/api/comment/all'
    ajax('GET', path, '', callback)
}

// 增加一个 weibo
var apiWeiboAdd = function(form, callback) {
    var path = '/api/weibo/add'
    ajax('POST', path, form, callback)
}


var apiCommentAdd = function(form, callback) {
    var path = '/api/comment/add'
    ajax('POST', path, form, callback)
}

var apiWeiboUpdate = function(form, callback) {
    var path = '/api/weibo/update'
    ajax('POST', path, form, callback)
}

var apiWeiboDelete = function(id,callback) {
    var path = `/api/weibo/delete?id=${id}`
    ajax('GET', path, '', callback)
}

// TODO DOM
var weiboTemplate = function(weibo) {
    var t = `
        <div class="weibo-cell" id = weibo${weibo.id}>
            <button data-id=${weibo.id} class="weibo-delete">删除</button>
            <button data-id=${weibo.id} class="weibo-edit">编辑</button>
            <span class= "weibo-content">${weibo.content}</span>
            <br>
            <span>评论</span>
            <br>
            <input id = 'id-input-comment'>
            <button data-id=${weibo.id} class="comment-add">添加评论</button>
        </div>

    `
//
//        <div class="comment-add" >
//            <input id='id-input-comment'>
//            <button id='id-comment-add'>添加评论</button>
//
//        </div>
    return t
}


var commentTemplate = function(comment) {
    var t = `
        <div class="comment-cell">
            <button data-id=${comment.id} class="comment-delete">删除</button>
            <button data-id=${comment.id} class="comment-edit">编辑</button>
            <span class= "comment-content">${comment.content}</span>
        </div>
    `
    return t
}


var weiboUpdateTemplate = function(weiboId) {
    var t = `
        <div class="weibo-update-form">
            <input class="weibo-update-input">
            <button data-id=${weiboId} class="weibo-update">更新</button>
        </div>
    `
    return t
}


var insertWeibo = function(weibo) {
    var weiboCell = weiboTemplate(weibo)
    // 插入 weibo-list
    var weiboList = e('.weibo-list')
    log('weibo-list',weiboList.dataset.id )
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}


var insertComment = function(comment) {
    var commentCell = commentTemplate(comment)
    var weiboId = comment.weibo_id
    //查找comment中对应的weibo_id
    log('weibo_id',weiboId)
    var weibo = e(`#weibo${weiboId}`)
    log('weibo',weibo)


    if (weibo == null){
        log('无评论')}
    else{
        var weibocell = weibo.closest('.weibocell')
        weibo.insertAdjacentHTML('beforeEnd', commentCell)}
//        edit_button.parentElement.insertAdjacentHTML('beforeend', editCell)
}


var insertUpdate = function(edit_button) {
    var weiboId = edit_button.dataset.id
    // 插入 weibo-list
    var editCell = weiboUpdateTemplate(weiboId)
    edit_button.parentElement.insertAdjacentHTML('beforeend', editCell)
}


var loadWeibos = function() {
    // 调用 ajax api 来载入数据
    apiWeiboAll(function(r) {
        console.log('load all', r)
        // 解析为 数组
        var weibos = JSON.parse(r)
        // 循环添加到页面中
        for(var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            insertWeibo(weibo)
        }
    })
}


var loadComments = function() {
    // 调用 ajax api 来载入数据
    apiCommentAll(function(r) {
        console.log('load all', r)
        // 解析为 数组
        var comments = JSON.parse(r)
        // 循环添加到页面中
        for(var i = 0; i < comments.length; i++) {
            var comment = comments[i]
            insertComment(comment)
        }
    })
}

var bindEventWeiboAdd = function() {
    var b = e('#id-button-add')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(){
        var input = e('#id-input-weibo')
        var content = input.value
        log('click add', content)
        var form = {
            content: content,
        }
        apiWeiboAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var weibo = JSON.parse(r)
            insertWeibo(weibo)
        })
    })
}


var bindEventCommentAdd = function(){
    var weiboList = e('.weibo-list')
    // 事件响应函数会被传入一个参数, 就是事件本身
    weiboList.addEventListener('click', function(event){

     // 我们可以通过 event.target 来得到被点击的元素
     var self = event.target

     // 判断是否拥有某个 class 的方法如下
     if (self.classList.contains('comment-add')) {
         log('点到了 添加评论按钮',self.dataset.id)
         var weiboCell = self.closest('.weibo-cell')
         var input = weiboCell.querySelector('#id-input-comment')
         var weiboId = self.dataset.id
         log('comment_weiboId',weiboId)
         var form = {
            weibo_id: weiboId,
            content: input.value,

         }
         log('form',form)
         apiCommentAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var comment = JSON.parse(r)
            insertComment(comment,self)
     })}
     else {
          log('点击的不是更新按钮******')
     }
 })}



var bindEventWeiboDelete = function(){
    var weiboList = e('.weibo-list')
    // 事件响应函数会被传入一个参数, 就是事件本身
    weiboList.addEventListener('click', function(event){
     // log('click weibolist', event)
     // 我们可以通过 event.target 来得到被点击的元素
     var self = event.target
     // log('被点击的元素是', self)
     // 通过比较被点击元素的 class 来判断元素是否是我们想要的
     // classList 属性保存了元素的所有 class
     // 在 HTML 中, 一个元素可以有多个 class, 用空格分开
     // log(self.classList)
     // 判断是否拥有某个 class 的方法如下
     if (self.classList.contains('weibo-delete')) {
         log('点到了 删除按钮',self.dataset.id)
         var weiboId = self.dataset.id
         // 删除 self 的父节点
         // parentElement 可以访问到元素的父节点

         apiWeiboDelete(weiboId,function(r) {
            self.parentElement.remove()
        })
     } else {
         // log('点击的不是删除按钮******')
     }
 })
}

var bindEventWeiboEdit = function(){
    var weiboList = e('.weibo-list')
    // 事件响应函数会被传入一个参数, 就是事件本身
    weiboList.addEventListener('click', function(event){
     // log('click weibolist', event)
     // 我们可以通过 event.target 来得到被点击的元素
     var self = event.target
     // log('被点击的元素是', self)
     // 通过比较被点击元素的 class 来判断元素是否是我们想要的
     // classList 属性保存了元素的所有 class
     // 在 HTML 中, 一个元素可以有多个 class, 用空格分开
     // log(self.classList)
     // 判断是否拥有某个 class 的方法如下
     if (self.classList.contains('weibo-edit')) {
         log('点到了 编辑按钮',self.dataset.id)
         var weiboId = self.dataset.id
         //插入编辑输入框
         insertUpdate(self)
     } else {
         // log('点击的不是吧编辑按钮******')
     }
 })

}

var bindEventWeiboUpdate = function(){
    var weiboList = e('.weibo-list')
    // 事件响应函数会被传入一个参数, 就是事件本身
    weiboList.addEventListener('click', function(event){

     // 我们可以通过 event.target 来得到被点击的元素
     var self = event.target

     // 判断是否拥有某个 class 的方法如下
     if (self.classList.contains('weibo-update')) {
         log('点到了 更新按钮',self.dataset.id)
         var weiboCell = self.closest('.weibo-cell')
         var input = weiboCell.querySelector('.weibo-update-input')
         var weiboId = self.dataset.id

         var form = {
            id: weiboId,
            content: input.value,

         }
         apiWeiboUpdate(form,function(r){
            log('收到更新数据',r)

            var updateForm = weiboCell.querySelector('.weibo-update-form')
            updateForm.remove()

            var weibo = JSON.parse(r)
            var weiboTask = weiboCell.querySelector('.weibo-content')
            weiboTask.innerText = weibo.content
         })
     } else {
         // log('点击的不是更新按钮******')
     }
 })

}

var bindEvents = function() {
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
    bindEventCommentAdd()

}

var __main = function() {
    bindEvents()
    loadWeibos()
    loadComments()
}

__main()