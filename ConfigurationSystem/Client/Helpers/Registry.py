# $HeadURL$
__RCSID__ = "$Id$"

from DIRAC import S_OK, S_ERROR
from DIRAC.Core.Utilities import List
from DIRAC.ConfigurationSystem.Client.Config import gConfig
from DIRAC.ConfigurationSystem.Client.Helpers.CSGlobals import getVO

g_BaseSecuritySection = "/Registry"

def getUsernameForDN( dn, usersList = False ):
  if not usersList:
    retVal = gConfig.getSections( "%s/Users" % g_BaseSecuritySection )
    if not retVal[ 'OK' ]:
      return retVal
    usersList = retVal[ 'Value' ]
  for username in usersList:
    if dn in gConfig.getValue( "%s/Users/%s/DN" % ( g_BaseSecuritySection, username ), [] ):
      return S_OK( username )
  return S_ERROR( "No username found for dn %s" % dn )

def getDNForUsername( username ):
  dnList = gConfig.getValue( "%s/Users/%s/DN" % ( g_BaseSecuritySection, username ), [] )
  if dnList:
    return S_OK( dnList )
  return S_ERROR( "No DN found for user %s" % username )

def getGroupsForUser( username ):
  retVal = gConfig.getSections( "%s/Groups" % g_BaseSecuritySection )
  if not retVal[ 'OK' ]:
    return retVal
  groupsList = retVal[ 'Value' ]
  userGroups = []
  for group in groupsList:
    if username in gConfig.getValue( "%s/Groups/%s/Users" % ( g_BaseSecuritySection, group ), [] ):
      userGroups.append( group )
  if not userGroups:
    return S_ERROR( "No groups found for user %s" % username )
  userGroups.sort()
  return S_OK( userGroups )

def getGroupsForDN( dn ):
  retVal = getUsernameForDN( dn )
  if not retVal[ 'OK' ]:
    return retVal
  return getGroupsForUser( retVal[ 'Value' ] )

def getHostnameForDN( dn ):
  retVal = gConfig.getSections( "%s/Hosts" % g_BaseSecuritySection )
  if not retVal[ 'OK' ]:
    return retVal
  hostList = retVal[ 'Value' ]
  for hostname in hostList:
    if dn in gConfig.getValue( "%s/Hosts/%s/DN" % ( g_BaseSecuritySection, hostname ), [] ):
      return S_OK( hostname )
  return S_ERROR( "No hostname found for dn %s" % dn )

def getDefaultUserGroup():
  return gConfig.getValue( "/%s/DefaultGroup" % g_BaseSecuritySection, "user" )

def getAllUsers():
  retVal = gConfig.getSections( "%s/Users" % g_BaseSecuritySection )
  if not retVal[ 'OK' ]:
    return []
  return retVal[ 'Value' ]

def getUsersInGroup( groupName, defaultValue = [] ):
  option = "%s/Groups/%s/Users" % ( g_BaseSecuritySection, groupName )
  return gConfig.getValue( option, defaultValue )

def getPropertiesForGroup( groupName, defaultValue = [] ):
  option = "%s/Groups/%s/Properties" % ( g_BaseSecuritySection, groupName )
  return gConfig.getValue( option, defaultValue )

def getPropertiesForHost( hostName, defaultValue = [] ):
  option = "%s/Hosts/%s/Properties" % ( g_BaseSecuritySection, hostName )
  return gConfig.getValue( option, defaultValue )

def getPropertiesForEntity( group, name = "", DN = "", defaultValue = [] ):
  if group == 'hosts':
    if not name:
      result = getHostnameForDN( DN )
      if not result[ 'OK' ]:
        return defaultValue
      name = result[ 'Value' ]
    return getPropertiesForHost( name, defaultValue )
  else:
    return getPropertiesForGroup( group, defaultValue )

def getBannedIPs():
  return gConfig.getValue( "%s/BannedIPs" % g_BaseSecuritySection, [] )

def getDefaultVOMSAttribute():
  return gConfig.getValue( "%s/DefaultVOMSAttribute" % g_BaseSecuritySection, "" )

def getVOMSAttributeForGroup( group ):
  return gConfig.getValue( "%s/Groups/%s/VOMSRole" % ( g_BaseSecuritySection, group ), getDefaultVOMSAttribute() )

def getDefaultVOMSVO():
  vomsVO = gConfig.getValue( "%s/DefaultVOMSVO" % g_BaseSecuritySection, "" )
  if vomsVO:
    return vomsVO
  return getVO()

def getVOMSVOForGroup( group ):
  return gConfig.getValue( "%s/Groups/%s/VOMSVO" % ( g_BaseSecuritySection, group ), getDefaultVOMSVO() )

def getGroupsWithVOMSAttribute( vomsAttr ):
  retVal = gConfig.getSections( "%s/Groups" % ( g_BaseSecuritySection ) )
  if not retVal[ 'OK' ]:
    return []
  groups = []
  for group in retVal[ 'Value' ]:
    if vomsAttr == gConfig.getValue( "%s/Groups/%s/VOMSRole" % ( g_BaseSecuritySection, group ), "" ):
      groups.append( group )
  return groups