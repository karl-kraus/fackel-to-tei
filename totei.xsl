<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">
    <xsl:template match="node()|@*">
        <xsl:copy>
            <xsl:apply-templates select="node()|@*"/>
        </xsl:copy>
    </xsl:template>
    <xsl:template match="DATE">
        <date><xsl:apply-templates/></date>
    </xsl:template>
    
    <xsl:template match="TAB"><space/></xsl:template>
    
   
    <xsl:template match="P">
        <p>
            <xsl:attribute name="ana"><xsl:value-of select="@parid"/></xsl:attribute><xsl:apply-templates/></p>
    </xsl:template>
    
    <xsl:template match="IN">
        <inciptit><xsl:apply-templates/></inciptit>
    </xsl:template>
    
    <xsl:template match="INSULT">
        <seg type="insult"><xsl:apply-templates/></seg>
    </xsl:template>
    
    <xsl:template match="ERR[@sug]">
        <choice><sic><xsl:apply-templates/></sic><corr><xsl:value-of select="@sug"/></corr></choice>
    </xsl:template>
    
    <xsl:template match="PERIODICAL">
        <rs><xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
            <xsl:if test="@globID">
            <xsl:attribute name="ana"><xsl:value-of select="@globID"/></xsl:attribute>
        </xsl:if><xsl:apply-templates/></rs>
    </xsl:template>
    
    <xsl:template match="LS"/>
    
    <xsl:template match="LE[preceding-sibling::*[1][self::HYPH1]]">
        <lb />
    </xsl:template>
    <xsl:template match="LE[not(preceding-sibling::*[1][self::HYPH1])]">
        <lb />
    </xsl:template>
    <xsl:template match="HYPH1"><xsl:value-of select="@content"/><xsl:value-of select="@cont"/></xsl:template>
    <xsl:template match="HYPH2"/>
    
    <xsl:template match="NAME">
        <rs>
            <xsl:attribute name="type"><xsl:value-of select="@cat"/></xsl:attribute>
            <xsl:if test="@globID">
                <xsl:attribute name="ana"><xsl:value-of select="@globID"/></xsl:attribute>
            </xsl:if>
        <xsl:apply-templates/>
        </rs>
    </xsl:template>
    <xsl:template match="NC">
        <rs>
            <xsl:attribute name="type">
                <xsl:value-of select="@cat"/>
            </xsl:attribute>
            <xsl:if test="@globID">
                <xsl:attribute name="ana"><xsl:value-of select="@globID"/></xsl:attribute>
            </xsl:if><xsl:apply-templates/>
        </rs>
    </xsl:template>
    <xsl:template match="LANG">
        <foreign>
            <xsl:attribute name="xml:lang"><xsl:value-of select="@iso"/></xsl:attribute><xsl:apply-templates/>
        </foreign>
    </xsl:template>
    <xsl:template match="LG">
        <lg><xsl:apply-templates/></lg>
    </xsl:template>
    <xsl:template match="L">
        <l><xsl:apply-templates/></l>
    </xsl:template>
    <xsl:template match="ABBR">
        <abbr><xsl:apply-templates/></abbr>
    </xsl:template>
    <xsl:template match="SPC">
        <seg type="spc"><xsl:apply-templates/></seg>
    </xsl:template>
    <xsl:template match="SIDEHEAD">
        <seg type="sidehead"><xsl:apply-templates/></seg>
    </xsl:template>
    <xsl:template match="I">
        <seg type="i"><xsl:apply-templates/></seg>
    </xsl:template>
    <xsl:template match="SYMBOL">
        <seg type="symbol">
            <xsl:attribute name="subtype">
                <xsl:value-of select="@type"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </seg>
    </xsl:template>
    <xsl:template match="SOURCE">
        <seg>
            <xsl:if test="@sourceName">
                <xsl:attribute name="source"><xsl:value-of select="."/></xsl:attribute>
            </xsl:if>
            <xsl:if test="@sourceID">
                <xsl:attribute name="ana"><xsl:value-of select="."/></xsl:attribute>
            </xsl:if>
        </seg>
    </xsl:template>
    <xsl:template match="TITLE"/>
    <xsl:template match="DIV_START"/>
    <xsl:template match="DIV_END"/>
    <xsl:template match="ELIDASH">
        <seg type="ELIDASH"><xsl:value-of select="@expan"/></seg>
    </xsl:template>
</xsl:stylesheet>