AliSoftVersion=VO_ALICE@AliPhysics::vAN-20190318_ROOT6-1

function tokeninit()
{
	# Obtain grid token and setup proxy
	alien-token-init
	source /tmp/gclient_env_`id -u $USER`
}



# Just enter the environment
eval `alienv printenv VO_ALICE@$AliSoftVersion`

# Enable python on lxplus
export PYTHONPATH=/lib
#/usr/lib64/root/:/usr/lib64/:/usr/lib/:/lib


# Check for token and get it if needed
alien-token-info || tokeninit

export PROMPT_PREFIX='\033[1;33m('$ALIPHYSICS_VERSION')\033[0m'
export PS1="$PROMPT_PREFIX $PS1"
