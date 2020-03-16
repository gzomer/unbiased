var _TEMPLATES = {
	alert : '<div data-testid="post_message" class="_5pbx userContent _3576" style="padding-bottom: 20px;padding-top: 10px;background: #fbeab6;margin-left: -12px;margin-right: -12px;margin-top: 0px;padding: 10px;"><p>The above post contains biased opinions. Here are some alternative views.</p></div>',
	suggestion : '<div class="clearfix _2r3x"> <div class="lfloat _ohe"> <span class="_3m6-"> <div class="_63yw"> <div class="_6ks"> <a href="$LINK$" aria-describedby="u_fetchstream_2_9" tabindex="-1" target="_blank" rel="noopener nofollow" data-lynx-mode="async"> <div class="_6l- __c_"> <div class="uiScaledImageContainer _6m5 fbStoryAttachmentImage" style="width: 100%;height: 120px;background: url(\'$IMAGE$\');background-repeat: no-repeat;background-size: auto;background-position: center;background-repeat: no-repeat;background-size: cover;"> </div> </div> </a> </div> </div> <div class="_3ekx _29_4"> <div class="_6m3 _--6"> <div class="_59tj _2iau"> <div> <div class="_6lz _6mb _1t62 ellipsis">$DOMAIN$</div> <div class=""></div> </div> </div> <div class="_3n1k"> <div class="mbs _6m6 _2cnj _5s6c"><a href="$LINK$" rel="noopener nofollow" target="_blank" data-lynx-mode="async">$TITLE$</a></div> <div class="_6m7 _3bt9"></div> </div> </div> <a href="$LINK$" aria-describedby="u_fetchstream_2_5" rel="noopener nofollow" tabindex="-1" target="_blank" class="_52c6" > <div class="accessible_elem" id="u_fetchstream_2_5">$DESCRIPTION$</div> </a> </div> </span> </div> <div class="_42ef"><span class="_3c21"></span></div> </div>',
	leftContent : '<div class="_6m2 _1zpr clearfix _dcs _4_w4 _41u- _59ap _2bf7 _64lx _3eqz _20pq _3eqw _2rk1 _359m _3n1j" style="width: 248px;display: inline-block;margin-right: 9px;border-right: 5px solid #ccc;">$CONTENT$</div>',
	rightContent: '<div class="_6m2 _1zpr clearfix _dcs _4_w4 _41u- _59ap _2bf7 _64lx _3eqz _20pq _3eqw _2rk1 _359m _3n1j" style="width: 249px;display: inline-block;border-right: 1px solid #ccc;">$CONTENT$</div>'
}

var _HEADLINE_CLASS = 'headlined-checked';

function sendMessage(message, cb){
	chrome.runtime.sendMessage(message, cb);
}

function hasSuggestions(response) {
	if (!response.success) {
		return false;
	}

	if (response.suggestions == null || response.suggestions.length == 0) {
		return false;
	}	
	return true;
}

function replaceVariables(template, variables) {
	if (typeof variables != 'undefined') {
		for ( var key in variables) {
			template = template.replace(new RegExp('\\$'+key.toUpperCase()+ '\\$', "gi"),variables[key]);
		}	
	}

	return template	
}
function convertTemplateToDOM(template, variables) {
	template = replaceVariables(template, variables);	
	return new DOMParser().parseFromString(template, 'text/html').body.firstChild;

}
function renderSuggestions(parent, suggestions) {

	var alert = convertTemplateToDOM(_TEMPLATES.alert);
	var suggestion1 =  replaceVariables(_TEMPLATES.suggestion, suggestions[0]);
	var suggestion2 =  replaceVariables(_TEMPLATES.suggestion, suggestions[1]);

	var leftContent = convertTemplateToDOM(_TEMPLATES.leftContent,{content : suggestion1})
	var rightContent = convertTemplateToDOM(_TEMPLATES.rightContent,{content : suggestion2})

	parent.appendChild(alert);
	parent.appendChild(leftContent);
	parent.appendChild(rightContent);
}

function getNewsHeadlines() {
	document.querySelectorAll('.mtm').forEach(function(e){	    
	    var headlineElement = e.querySelector('.mbs a');

	    if (typeof headlineElement === 'undefined' || headlineElement == null) {
	    	return;
	    }

	    if (headlineElement.classList.contains(_HEADLINE_CLASS)) {
	    	return;
	    }	    

	    headlineElement.classList.toggle(_HEADLINE_CLASS);

	    var headline = headlineElement.textContent;
	    sendMessage({action:'suggestions', headline:headline}, function(response) {	    	
	    	if (!hasSuggestions(response)) {
	    		return;
	    	}		
	    	renderSuggestions(e, response.suggestions);
	    });
	})
};

setInterval(function(){
	getNewsHeadlines();
},500)