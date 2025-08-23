/**
 * $Id: editor_plugin_src.js 520 2008-01-07 16:30:32Z adam.wulf $
 *
 * @author Adam Wulf http://welcome.totheinter.net/
 */

(function() {
	tinymce.create('tinymce.plugins.DuplicatePlugin', {
	
		 /**
		  * This function will return the number
		  * of times that the findMe node occurs
		  * inside of the DOM
		  * @param n: the node to look inside of
		  * @param findMe: the node to find
		  * @return: the number of times findMe is found
		  *          inside of n
		  */
		 countOccurances : function(n, findMe){
		 	if(n == findMe) return 1;
		 	if(n.nodeType != 1) return 0;
		 	var ret = 0;
		 	for(var i=0;i<n.childNodes.length;i++){
		 		ret += this.countOccurances(n.childNodes[i], findMe);
		 	}
		 	return ret;
		 },
		 
		 /**
		  * returns a simplified XML representation of
		  * the input node n. an attribute "count"
		  * will be added to every node, and its value
		  * will be the number of times that that node
		  * appears in the entire DOM
		  *
		  * invalid nodes are also changed to display in red text
		  *
		  * @param n: the node to convert to XML
		  * @param indent: the string of empty spaces
		  *                to be used to indent the XML
		  * @param ed: the TinyMCE Editor
		  * @return: an XML (ish) string of n
		  * @sideeffect: invalid nodes are changed to red text
		  */
		 toXML : function(n, indent, ed){
            if(n.nodeType == 3) return indent + n.nodeValue + "\n";
            var ret = "";
            if(n.nodeName.toLowerCase() == "br"){
                return ret + indent + "<BR>\n";
            }
            ret += indent + "<" + n.nodeName + " count=" + this.countOccurances(ed.getBody(), n) + ">\n";
            for(var i=0;i<n.childNodes.length;i++){
                var invalidParent = (n != n.childNodes[i].parentNode);
                if(invalidParent) ret += indent + "  <error>\n";
                ret += this.toXML(n.childNodes[i], indent + (invalidParent ? "    " : "  "), ed);
                if(invalidParent) ret += indent + "  </error>\n";
                
                if(invalidParent) n.childNodes[i].style.color = "red";
            }
            ret += indent + "</" + n.nodeName + ">\n";
            return ret;
        },
        
        /**
         * validates the Editor's <body> to try and find
         * duplicate nodes. This function relies on the user
         * copying and pasting the sample.rtf from
         * http://welcome.totheinter.net/2009/07/21/the-undocumented-life-of-javascripts-parentnode-property-internet-explorer-edition/
         *
         * A textarea with id #theContents is assumed, and
         * the XML representation of the <body> is added there.
         *
         * also, to show that jQuery also shows the problem, a
         * brief message will be shown at the top of the XML output
         * describing if jQuery also selected an invalid child.
         *
         * @param ed: TinyMCE Editor
         * @return: nothing
         * @sideeffect: contents of #theContents modified
         */
        validate : function(ed){
        	var jQueryText = "jQuery only selected valid children!\n\n";
        	
    		var parent = $(ed.getBody()).find("p span").get(0);
    		if(parent){
				var kids = $(ed.getBody()).find("p span").children();
				for(var i=0;i<kids.length;i++){
					var kid = kids.get(i);
					if(kid.parentNode != parent){
						jQueryText = "jQuery selected invalid children as well!\n\n";
					}
				}
    		}

			$("#theContents").val(jQueryText + this.toXML(ed.getBody(), "", ed));
        },
	
		/**
		 * initialize the plugin.
		 *
		 * add the custom command, button,
		 * and nodeChange handler
		 */
		init : function(ed, url) {

			// Register commands
			ed.addCommand('mceFindDuplicates', function() {
				this.validate(ed);
			}, this);

			// Register buttons
			ed.addButton('validate', {
				label : 'validate', 
				cmd : 'mceFindDuplicates'
			});

			ed.onNodeChange.add(function(ed, cm, n) {
				this.validate(ed);
			}, this);

		},

		getInfo : function() {
			return {
				longname : 'Duplicate',
				author : 'Adam Wulf',
				authorurl : 'http://welcome.totheinter.net',
				infourl : 'http://welcome.totheinter.net',
				version : "1.0.0"
			};
		}
	});

	// Register plugin
	tinymce.PluginManager.add('duplicate', tinymce.plugins.DuplicatePlugin);
})();