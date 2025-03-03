/*
vim: syntax=groovy
-*- mode: groovy;-*-
*/


/*
*******************************************************************************
* version_check
*******************************************************************************
 */
def version_check(required_ver, current_ver){
	
	try {
	    if( ! current_ver.matches(">= $required_ver") ){
		throw GroovyException('Nextflow version too old')
	    }
	} catch (all) {
		log.error "Error: Nextflow version $required_ver required! " +
		      "You are running version $current_ver.\n" +
		      "Please update Nextflow.\n" 
		exit 1
		
	}
}


/*
*******************************************************************************
* Function to show yes/no prompt
*******************************************************************************
 */
def prompt(input){

	if(input == "n"){
		exit 1
	}
	if(input == "y"){
		return(true)
	}
	if(input != "n" || input!= "y"){
		println "Please use 'y' for yes and 'n' for no."		
		prompt(System.console().readLine 'Do you want to continue again (y/n)?')
	}
}



