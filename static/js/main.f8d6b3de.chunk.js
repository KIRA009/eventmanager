(window.webpackJsonp=window.webpackJsonp||[]).push([[8],{105:function(e,t,n){},107:function(e,t,n){},108:function(e,t,n){},110:function(e,t,n){"use strict";n.r(t);var r=n(69),a=n(0),o=n.n(a),c=n(21),u=n.n(c),i=n(14),l=n(63),s=n(20),d=n(28),p=n(29),f=n(31),m=n(30),y=n(32),g=(n(105),n(106),n(23)),h=n(127),b=n(128),E=n(45),O=n(17),j=(n(107),n(111)),v=n(24),P=(n(72),n(3)),k=n(19),T=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(3),n.e(4),n.e(6),n.e(15)]).then(n.bind(null,632))}),I=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(1),n.e(3),n.e(4),n.e(10)]).then(n.bind(null,1064))}),_=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(1),n.e(3),n.e(2),n.e(16)]).then(n.bind(null,1069))}),S=Object(a.lazy)(function(){return n.e(29).then(n.bind(null,741))}),L=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(1),n.e(2),n.e(25)]).then(n.bind(null,1052))}),R=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(1),n.e(2),n.e(21)]).then(n.bind(null,1053))}),C=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(1),n.e(2),n.e(20)]).then(n.bind(null,1054))}),A=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(1),n.e(2),n.e(17)]).then(n.bind(null,1070))}),D=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(1),n.e(2),n.e(22)]).then(n.bind(null,1055))}),w=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(1),n.e(2),n.e(23)]).then(n.bind(null,1056))}),N=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(1),n.e(3),n.e(4),n.e(12)]).then(n.bind(null,1065))}),G=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(1),n.e(3),n.e(4),n.e(11)]).then(n.bind(null,1067))}),x=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(1),n.e(2),n.e(27)]).then(n.bind(null,1057))}),z=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(3),n.e(4),n.e(28),n.e(19)]).then(n.bind(null,1058))}),U=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(2),n.e(5),n.e(31)]).then(n.bind(null,1059))}),H=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(2),n.e(5),n.e(30)]).then(n.bind(null,1060))}),B=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(1),n.e(6),n.e(7),n.e(13)]).then(n.bind(null,1061))}),F=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(7),n.e(18)]).then(n.bind(null,742))}),M=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(1),n.e(2),n.e(24)]).then(n.bind(null,1062))}),V=Object(a.lazy)(function(){return Promise.all([n.e(0),n.e(1),n.e(2),n.e(26)]).then(n.bind(null,1063))});O.c.configure();var q=function(e){function t(e){var n;return Object(d.a)(this,t),(n=Object(f.a)(this,Object(m.a)(t).call(this,e))).state={},n}return Object(y.a)(t,e),Object(p.a)(t,[{key:"componentWillMount",value:function(){var e=window.localStorage.getItem(k.j);null==e||v.a.setToken(e),this.props.onLoad(e?1:null,e)}},{key:"componentWillReceiveProps",value:function(e){this.props.history.location!==e.history.location&&this.props.onRedirect(e.history.location),e.redirectTo&&e.redirectTo!==this.props.redirectTo&&s.c.dispatch(Object(E.a)(e.redirectTo)),e.user&&this.setState({user:e.user})}},{key:"render",value:function(){return o.a.createElement("div",{style:{height:"100%"}},o.a.createElement(o.a.Suspense,{fallback:o.a.createElement("div",{style:{width:"40px",height:"40px",position:"fixed",top:"50%",left:"50%",transform:"translate(-50%,-50%)"}},o.a.createElement("h4",null,"Loading..."),o.a.createElement(j.a,null))},o.a.createElement(g.a,{history:this.props.history},o.a.createElement(h.a,null,o.a.createElement(b.a,{path:"/",component:_,exact:!0}),o.a.createElement(b.a,{path:"/privacy-policy",component:L,exact:!0}),o.a.createElement(b.a,{path:"/refund-policy",component:V,exact:!0}),o.a.createElement(b.a,{path:"/terms-and-conditions",component:x,exact:!0}),o.a.createElement(b.a,{path:"/login",component:R,exact:!0}),o.a.createElement(b.a,{path:"/signup",component:C,exact:!0}),o.a.createElement(b.a,{path:"/admin",component:I,exact:!0}),o.a.createElement(b.a,{path:"/faqs",component:A,exact:!0}),o.a.createElement(b.a,{path:"/contact-us/",component:M,exact:!0}),o.a.createElement(b.a,{path:"/purchase",component:D,exact:!0}),o.a.createElement(b.a,{path:"/purchase/result",component:w,exact:!0}),o.a.createElement(b.a,{path:"/order-history/",component:N,exact:!0}),o.a.createElement(b.a,{path:"/admin/products/",component:G,exact:!0}),o.a.createElement(b.a,{path:"/admin/products/sold-products/",component:F,exact:!0}),o.a.createElement(b.a,{path:"/admin/payments/",component:B,exact:!0}),o.a.createElement(b.a,{path:"/pricing",component:S,exact:!0}),o.a.createElement(b.a,{path:"/user-payment/",component:z,exact:!0}),o.a.createElement(b.a,{path:"/user-payment/success/",component:U,exact:!0}),o.a.createElement(b.a,{path:"/user-payment/fail/",component:H,exact:!0}),o.a.createElement(b.a,{path:"/:userName/",component:T,exact:!0}),o.a.createElement(b.a,{path:"*"},o.a.createElement(K,null))))),void 0,void 0,o.a.createElement(O.b,{autoClose:2e3,closeOnClick:!0,transition:O.a,pauseOnFocusLoss:!1,position:"top-right"}))}}]),t}(a.Component);function K(){return o.a.createElement("div",null,o.a.createElement("h3",null,"No match for"))}var W=Object(i.c)(function(e){return{appLoaded:e.common.appLoaded,appName:e.common.appName,currentUser:e.common.currentUser,redirectTo:e.common.redirectTo,apiKey:e.common.apiKey,user:e.AuthReducer.user}},function(e){return{onLoad:function(t,n){return e({type:P.b,payload:t,apiKey:n,skipTracking:!0})},onRedirect:function(t){return e({type:P.E,payload:t})},clearReducer:function(){return e({type:"CLEAR"})},setUser:function(t){return e({type:P.J,payload:t})}}})(q);n(108),Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));u.a.render(o.a.createElement(i.a,{store:s.c},o.a.createElement(l.a,{loading:null,persistor:s.b},o.a.createElement(r.AppContainer,null,o.a.createElement(W,{history:s.a})))),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then(function(e){e.unregister()})},19:function(e,t,n){"use strict";n.d(t,"j",function(){return r}),n.d(t,"i",function(){return a}),n.d(t,"b",function(){return o}),n.d(t,"a",function(){return c}),n.d(t,"c",function(){return u}),n.d(t,"f",function(){return i}),n.d(t,"g",function(){return l}),n.d(t,"h",function(){return s}),n.d(t,"d",function(){return d}),n.d(t,"e",function(){return p});var r="EVENT_MANAGER_TOKEN",a="EVENT_MANAGER_USER_DETAILS",o="",c="MyWebLink",u=JSON.stringify({backgroundColor:"#7f5a83",backgroundImage:"linear-gradient(315deg, #7f5a83 0%, #0d324d 74%)"}),i="ESTIMATED_DELIVERY",l="IS_COD_AVAILABLE",s="IS_ONLINE_PAYMENT_AVAILABLE",d="#fff",p=0},20:function(e,t,n){"use strict";var r=n(8),a=(n(64),n(65)),o=n(60),c=n(43),u=n(66),i=n.n(u),l=n(70),s=n(17),d=n(6),p=n(24),f=n(3),m=n(19);var y=function(e){return function(t){return function(n){if((o=n.payload)&&"function"===typeof o.then){e.dispatch({type:f.d,subtype:n.type});var r=e.getState().viewChangeCounter,a=n.skipTracking;n.payload.then(function(t){var o=e.getState();(a||o.viewChangeCounter===r)&&(n.payload=t.data,e.dispatch({type:f.c,promise:n.payload}),e.dispatch(n))},function(t){var o;console.log(t);var c="Check your Connection";t.response?(console.log(t.response.data),t.response.data.error&&(c=t.response.data.error),o=t.response.status):t.request?console.log(t.request):console.log("Error",t.message);var u=e.getState();if(a||u.viewChangeCounter===r){if(404===o){try{s.c.error(c),e.dispatch(Object(d.d)("/"))}catch(i){console.debug(i)}console.debug("ERRIIOIIO-----\x3e",t.response.status),n.payload=t.response.data,e.dispatch(n)}if(n.error=!0,t.response?n.payload=t.response.body||{}:n.payload={},n.skipTracking||e.dispatch({type:f.c,promise:n.payload}),n.type===f.C||401!==o&&403!==o)try{s.c.error(c)}catch(i){console.debug(i)}else{try{s.c.error("Token Expired. Login Again!!!")}catch(i){console.log("error ",t.response)}e.dispatch({type:f.D,promise:n.payload})}}})}else{var o;t(n)}}}},g=function(e){return function(t){return function(n){n.type===f.F||n.type===f.C?n.error||(window.localStorage.setItem(m.j,n.payload.data.token),p.a.setToken(n.payload.data.token)):n.type===f.J?window.localStorage.setItem(m.i,n.payload.user.username):n.type===f.D&&(window.localStorage.clear(),e.dispatch(Object(d.d)("/")),p.a.setToken(null)),t(n)}}},h=n(4),b=n(23),E=n(15),O={AuthReducer:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},t=arguments.length>1?arguments[1]:void 0;switch(t.type){case f.d:case f.c:return Object(h.a)({},e);case f.J:return Object(h.a)({},e,{user:t.payload});case f.k:return Object(h.a)({},e,{colleges:t.payload});case f.B:return Object(h.a)({},e,{user:t.payload});default:return e}return e},HomePageReducers:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},t=arguments.length>1?arguments[1]:void 0;switch(t.type){case f.a:if(e.cartItems&&e.cartItems.length>0){var n=!1,r=e.cartItems.map(function(e){return e.item.id===t.payload.item.id&&e.selectedSize===t.payload.selectedSize?(n=!0,Object(h.a)({},t.payload,{quantity:t.payload.quantity+e.quantity})):e});return n||(r=[t.payload].concat(Object(E.a)(r))),Object(h.a)({},e,{cartItems:r})}return Object(h.a)({},e,{cartItems:[t.payload]});case f.G:var a=e.cartItems.filter(function(e){return!(e.item.id===t.payload.item.id&&e.selectedSize===t.payload.selectedSize)});return Object(h.a)({},e,{cartItems:a});case f.f:return Object(h.a)({},e,{cartItems:[]});case f.v:return Object(h.a)({},e,{publicHeaderInfo:t.payload.feature});case f.y:return Object(h.a)({},e,{publicPageUser:t.payload.user});case f.w:return e.publicPageProducts?Object(h.a)({},e,{publicPageProducts:1===t.pageNumber?t.payload.products:[].concat(Object(E.a)(e.publicPageProducts),Object(E.a)(t.payload.products))}):Object(h.a)({},e,{publicPageProducts:t.payload.products});case f.x:return Object(h.a)({},e,{publicPageShopDetails:t.payload});default:return e}return e},AdminPageReducers:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},t=arguments.length>1?arguments[1]:void 0;switch(t.type){case f.d:case f.c:return Object(h.a)({},e);case f.n:return Object(h.a)({},e,{links:t.payload});case f.H:if(e.linkInfo&&e.linkInfo.length>0){var n=e.linkInfo.filter(function(e){return e.id!==t.payload.id});return Object(h.a)({},e,{linkInfo:[].concat(Object(E.a)(n),[t.payload])})}return Object(h.a)({},e,{linkInfo:[t.payload]});case f.g:return e.linkInfo?Object(h.a)({},e,{linkInfo:e.linkInfo.filter(function(e){return e.id!==t.payload.id})}):Object(h.a)({},e,{linkInfo:[]});case f.i:return Object(h.a)({},e,{homeBgStyle:t.payload});case f.m:return Object(h.a)({},e,{headerInfo:t.payload.feature});case f.o:return Object(h.a)({},e,{linkClicks:t.payload});case f.u:return Object(h.a)({},e,{profileViews:t.payload});default:return e}},PurchaseReducers:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},t=arguments.length>1?arguments[1]:void 0;switch(t.type){case f.e:return Object(h.a)({},e,{choosenPlan:t.payload});case f.s:return Object(h.a)({},e,{plans:t.payload.packs});default:return e}},OrderHistoryReducers:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},t=arguments.length>1?arguments[1]:void 0;switch(t.type){case f.q:return Object(h.a)({},e,{orderHistory:t.payload});default:return e}},ProductsPageReducers:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},t=arguments.length>1?arguments[1]:void 0;switch(t.type){case f.t:return e.products?Object(h.a)({},e,{products:1===t.pageNumber?t.payload.products:[].concat(Object(E.a)(e.products),Object(E.a)(t.payload.products))}):Object(h.a)({},e,{products:t.payload.products});case f.I:return Object(h.a)({},e,{products:t.payload.products});case f.A:return Object(h.a)({},e,{shopDetails:t.payload});case f.j:return Object(h.a)({},e,{categories:t.payload.categories});default:return e}},SoldProductsReducers:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},t=arguments.length>1?arguments[1]:void 0;switch(t.type){case f.p:return Object(h.a)({},e,{notDeliveredSoldProducts:t.payload.orders,notDeliveredProductsPageCount:t.payload.num_pages});case f.l:return Object(h.a)({},e,{deliveredSoldProducts:t.payload.orders,deliveredProductsPageCount:t.payload.num_pages});default:return e}},PaymentsReducers:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},t=arguments.length>1?arguments[1]:void 0;switch(t.type){case f.r:return Object(h.a)({},e,{pendingPayment:t.payload.amount});case f.z:return Object(h.a)({},e,{paymentRedeemHistory:t.payload.history});case f.h:return Object(h.a)({},e,{bankDetails:t.payload.seller});default:return e}}},j={appName:"ProjectX",token:null,viewChangeCounter:0},v=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:j,t=arguments.length>1?arguments[1]:void 0;switch(t.type){case f.b:return Object(h.a)({},e,{token:t.token||null,appLoaded:!0});case f.E:return console.log("red",t),Object(h.a)({},e,{redirectTo:t.payload});case f.F:return Object(h.a)({},e,{redirectTo:t.error?null:"/",token:t.error?null:t.payload.token,currentUser:t.error?null:t.payload.data.name,role:t.payload.role,name:t.payload.name});default:return e}};n.d(t,"a",function(){return T}),n.d(t,"c",function(){return S}),n.d(t,"b",function(){return L});var P,k={key:"root",storage:i.a,blacklist:["router"]},T=Object(l.a)({basename:m.b}),I=Object(c.a)(k,(P=T,function(e,t){if("LOGOUT"===t.type){var n=e,a=n.router,o=n.common;console.log(o),e={router:a,common:o}}return function(e){return Object(r.combineReducers)(Object(h.a)({},O,{common:v,router:Object(b.b)(e)}))}(P)(e,t)})),_=Object(o.a)(T),S=Object(r.createStore)(I,Object(a.composeWithDevTools)(Object(r.applyMiddleware)(_,y,g))),L=Object(c.b)(S)},24:function(e,t,n){"use strict";var r=n(13),a=n.n(r);a.a.defaults.baseURL="https://myweblink.store",a.a.defaults.timeout=88800,a.a.defaults.headers={};var o=function(e){return e},c={delete:function(e,t){return a.a.delete("".concat(e),{data:t}).then(o)},get:function(e){return a.a.get("".concat(e)).then(o)},getPaginated:function(e,t){return a.a.get("".concat(e)).set("page_num",t).then(o)},put:function(e,t){return a.a.put("".concat(e),t).then(o)},post:function(e,t){return a.a.post("".concat(e),t).then(o)},postFile:function(e,t){var n=new FormData;return t.forEach(function(e){n.append(e.key,e.file)}),a.a.post("".concat(e),n,{headers:{"Content-Type":"multipart/form-data"}}).then(o)}},u={login:function(e){return c.post("/api/login/",e)},logout:function(){return c.post("/api/logout/")},register:function(e){return c.post("/api/register/",e)},getColleges:function(){return c.get("/api/colleges/")},uploadProfileImage:function(e){return c.postFile("/api/upload/profile/",e)},getUserDetails:function(e){return c.post("/api/user/",e)},sendVerificationEmail:function(e){return c.post("/api/validate-email/",e)}},i={createLink:function(e){return c.post("/api/links/",e)},deleteLink:function(e){return c.delete("/api/links/",e)},getLinks:function(){return c.get("/api/links/")},updateLinkSequence:function(e){return c.post("/api/update-link-sequence/",e)},uploadLinkIcon:function(e){return c.postFile("/api/upload-icon/",e)},getHeaderInfo:function(e){return c.post("/pro/feature/",e)},uploadHeaderInfo:function(e){return c.postFile("/pro/feature/header/",e)},uploadBackground:function(e){return c.postFile("/pro/background/set/",e)},getBackground:function(e){return c.post("/pro/background/get/",e)},updateUserDetails:function(e){return c.post("/api/update/user/",e)},getLinkClicks:function(){return c.get("/analytics/get_clicks/")},getProfileViews:function(){return c.get("/analytics/get_views/")},addClickToLink:function(e){return c.post("/analytics/click/",e)},addViewToProfile:function(e){return c.post("/analytics/view/",e)}},l={createSubscription:function(e){return c.post("/payment/subscribe/",e)},getPlans:function(){return c.get("/api/packs/")}},s={getOrders:function(){return c.get("/payment/order/")},orderUnsubscribe:function(e){return c.post("/payment/cancel/",e)}},d={getProducts:function(e,t){return c.post("/pro/products/get/?pageNo=".concat(t),e)},createProduct:function(e){return c.post("/pro/product/create/",e)},updateProduct:function(e){return c.post("/pro/product/update/",e)},addProductImage:function(e){return c.postFile("/pro/product/image/add/",e)},deleteProductImage:function(e){return c.post("/pro/product/image/del/",e)},deleteProduct:function(e){return c.post("/pro/product/delete/",e)},makeOrder:function(e){return c.post("/payment/order/",e)},getShopDetails:function(e){return c.post("/pro/shop/get/",e)},setShippingAddress:function(e){return c.post("/pro/shipping/set/",e)},getCategories:function(e){return c.post("/pro/categories/get/",e)},deleteCategpry:function(e){return c.post("/pro/category/del/",e)}},p={getNotDeliveredSoldProducts:function(e){return c.get("/payment/products/sold/get/?pageNo=".concat(e,"&delivered=false"))},getDeliveredSoldProducts:function(e){return c.get("/payment/products/sold/get/?pageNo=".concat(e))},updateOrderStatus:function(e){return c.post("/payment/products/sold/update/",e)},initiateRefund:function(e){return c.post("/payment/order/refund/",e)}},f={setBankingDetails:function(e){return c.post("/pro/banking/set/",e)},redeemAmount:function(e){return c.post("/pro/pending/retrieve/",e)},getPendingPayment:function(){return c.get("/pro/pending/get/")},getRedeemHistory:function(){return c.get("/pro/pending/history/")},getBankDetails:function(){return c.get("/pro/banking/get/")}};t.a={Auth:u,setToken:function(e){a.a.defaults.headers.common={token:e}},AdminPage:i,requests:c,Purchase:l,OrderHistory:s,ProductsPage:d,SoldProducts:p,Payments:f}},3:function(e,t,n){"use strict";n.d(t,"b",function(){return r}),n.d(t,"E",function(){return a}),n.d(t,"C",function(){return o}),n.d(t,"D",function(){return c}),n.d(t,"F",function(){return u}),n.d(t,"d",function(){return i}),n.d(t,"c",function(){return l}),n.d(t,"k",function(){return s}),n.d(t,"J",function(){return d}),n.d(t,"B",function(){return p}),n.d(t,"n",function(){return f}),n.d(t,"m",function(){return m}),n.d(t,"H",function(){return y}),n.d(t,"g",function(){return g}),n.d(t,"i",function(){return h}),n.d(t,"e",function(){return b}),n.d(t,"o",function(){return E}),n.d(t,"u",function(){return O}),n.d(t,"s",function(){return j}),n.d(t,"q",function(){return v}),n.d(t,"t",function(){return P}),n.d(t,"a",function(){return k}),n.d(t,"G",function(){return T}),n.d(t,"f",function(){return I}),n.d(t,"r",function(){return _}),n.d(t,"z",function(){return S}),n.d(t,"h",function(){return L}),n.d(t,"p",function(){return R}),n.d(t,"l",function(){return C}),n.d(t,"I",function(){return A}),n.d(t,"A",function(){return D}),n.d(t,"x",function(){return w}),n.d(t,"v",function(){return N}),n.d(t,"y",function(){return G}),n.d(t,"w",function(){return x}),n.d(t,"j",function(){return z});var r="APP_LOAD",a="REDIRECT",o="LOGIN",c="LOGOUT",u="REGISTER",i="ASYNC_START",l="ASYNC_END",s="GET_COLLEGES",d="SET_USER",p="GET_USER_DETAILS",f="GET_LINKS",m="GET_HEADER_INFO",y="SET_LINK_INFO",g="DELETE_LINK_INFO",h="GET_BG_STYLE",b="CHOOSE_PURCHASE",E="GET_LINK_CLICKS",O="GET_PROFILE_VIEWS",j="GET_PLANS",v="GET_ORDER_HISTORY",P="GET_PRODUCTS",k="ADD_TO_CART",T="REMOVE_FROM_CART",I="CLEAR_CART",_="GET_PENDING_PAYMENT",S="GET_REDEEM_HISTORY",L="GET_BANK_DETAILS",R="GET_NOT_DELIVERED_SOLD_PRODUCTS",C="GET_DELIVERED_SOLD_PRODUCTS",A="SET_PRODUCTS",D="GET_SHOP_DETAILS",w="GET_PUBLIC_PAGE_SHOP_DETAILS",N="GET_PUBLIC_PAGE_HEADER_INFO",G="GET_PUBLIC_PAGE_USER",x="GET_PUBLIC_PAGE_PRODUCTS",z="GET_CATEGORIES"},72:function(e,t,n){"use strict";var r=n(28),a=n(29),o=n(31),c=n(30),u=n(33),i=n(32),l=n(0),s=n.n(l),d=n(14),p=n(111),f=(n(71),function(e){function t(e){var n;return Object(r.a)(this,t),(n=Object(o.a)(this,Object(c.a)(t).call(this,e))).state={progress:0},n.startLoader=n.startLoader.bind(Object(u.a)(n)),n}return Object(i.a)(t,e),Object(a.a)(t,[{key:"componentWillMount",value:function(){this.startLoader()}},{key:"startLoader",value:function(){var e=0,t=.1,n=setInterval(function(){e+=t;var r=Math.round(Math.atan(e)/(Math.PI/2)*100*1e3)/1e3,a=document.getElementById("progress-loading");a?(a.innerText=Math.floor(r),r>=100?clearInterval(n):r>=70&&(t=.1)):clearInterval(n)},100)}},{key:"render",value:function(){this.state.progress.progress;return s.a.createElement("div",{className:"loading"}," ",s.a.createElement("h1",{id:"progress-loading","aria-valuenow":0}," 85"),s.a.createElement(p.a,{style:{width:"40px",height:"40px"}}))}}]),t}(l.Component));t.a=Object(d.c)(function(e){return{}},function(e){return{}})(f)},76:function(e,t,n){e.exports=n(110)}},[[76,9,14]]]);
//# sourceMappingURL=main.f8d6b3de.chunk.js.map