(window.webpackJsonp=window.webpackJsonp||[]).push([[30],{1060:function(e,t,a){"use strict";a.r(t);var n=a(28),r=a(29),l=a(31),o=a(30),s=a(32),c=a(0),i=a.n(c),u=a(14),p=(a(71),a(45)),m=(a(179),a(746)),d=a.n(m),g=a(24),h=a(72),f=a(145),y=a(20),b=a(3),v=a(745),E=a.n(v),w=a(19),P=(a(196),function(e){function t(e){var a;return Object(n.a)(this,t),(a=Object(l.a)(this,Object(o.a)(t).call(this,e))).state={img:null,loading:!1,user:{profile_pic:null,link:[],username:""},error:"",bgStyle:null,togelSignUpMessage:!0,textColor:w.d,products:[],render:!1},a.links=[],a.cartItems=[],a}return Object(s.a)(t,e),Object(r.a)(t,[{key:"componentWillMount",value:function(){this.props.publicPageUser&&this.setState({user:this.props.publicPageUser})}},{key:"componentWillReceiveProps",value:function(e){e.publicPageUser&&this.setState({user:e.publicPageUser})}},{key:"render",value:function(){var e=this.state,t=e.user,a=(e.profile_pic,this.state.textColor);return i.a.createElement("div",{className:" "},i.a.createElement("div",{className:"home-page-nav-div"},i.a.createElement(f.a,{logostyles:{display:"flex",flexDirection:"row",color:this.state.textColor},parent:this.props.parent?this.props.parent:"public-home-page",username:t.username}),i.a.createElement("button",{className:"home-page-cart-div relative",type:"button",onClick:function(){return y.c.dispatch(Object(p.a)("/".concat(t.username)))}},i.a.createElement(d.a,{style:{color:"white"}}),i.a.createElement("span",{style:{color:a,fontWeight:"bold"}},"Home"))),i.a.createElement("div",{className:" payment-output "},i.a.createElement("div",{className:"dyna-width"},i.a.createElement("div",{className:" center"},i.a.createElement("article",{className:"payment-output-main-div"},i.a.createElement("div",{className:"logo-div"},i.a.createElement(f.a,{logostyles:{display:"flex",flexDirection:"row",margin:"auto",color:"black"},parent:this.props.parent?this.props.parent:"public-home-page",username:t.username})),i.a.createElement("img",{src:E.a}),i.a.createElement("h2",null," Payment Failed  "),i.a.createElement("p",null,"Sorry , We are facing some issue, It will get resolved shortly."),i.a.createElement("p",null,"If some money is deducted from your account then money will get transferred to our account within 5-7 working days."),i.a.createElement("p",null,"Please try after some time."),i.a.createElement("p",null,"Thank you for shopping with us."),i.a.createElement("button",{className:" relative",type:"button",onClick:function(){return y.c.dispatch(Object(p.a)("/".concat(t.username)))}},i.a.createElement(d.a,null),i.a.createElement("span",{style:{fontWeight:"bold"}},"Go To Home")))))),this.state.loading?i.a.createElement(h.a,null):null)}}]),t}(c.Component));t.default=Object(u.c)(function(e){return{publicPageUser:e.HomePageReducers.publicPageUser}},function(e){return{getUserDetails:function(e){return y.c.dispatch({type:b.B,payload:g.a.Auth.getUserDetails(e)})},getPublicPageHeaderInfo:function(t){return e({type:b.v,payload:g.a.AdminPage.getHeaderInfo(t)})}}})(P)}}]);
//# sourceMappingURL=30.577a724e.chunk.js.map