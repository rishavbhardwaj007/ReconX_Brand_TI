# utils/openai_analysis.py

import os
import json
import requests
from datetime import datetime

def analyze_with_openai(brand, results_data):
    """
    Analyze scan results using OpenAI to provide intelligent insights
    """
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        return "OpenAI API key not configured. Set OPENAI_API_KEY in your .env file."
    
    # Prepare data summary for analysis
    summary = prepare_data_summary(brand, results_data)
    
    prompt = f"""
    Analyze the following cybersecurity reconnaissance data for the brand "{brand}":

    {summary}

    Please provide:
    1. Risk Assessment (High/Medium/Low) with justification
    2. Key Security Concerns identified
    3. Immediate Action Items
    4. Long-term Recommendations
    5. Executive Summary (2-3 sentences)

    Focus on actionable insights and prioritize based on potential impact.
    """

    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-4',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a cybersecurity expert analyzing reconnaissance data. Provide clear, actionable insights focused on security risks and mitigation strategies.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': 1000,
                'temperature': 0.3
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"OpenAI API error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"

def prepare_data_summary(brand, results_data):
    """
    Prepare a concise summary of scan results for OpenAI analysis
    """
    summary = f"Brand: {brand}\n"
    summary += f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # GitHub Results
    github_count = len(results_data.get('github', []))
    summary += f"GitHub Leaks: {github_count} potential leaks found\n"
    if github_count > 0:
        summary += "  - Files containing brand mentions in public repositories\n"
    
    # Shodan Results
    shodan_results = results_data.get('shodan', '')
    if shodan_results and "found on Shodan" in shodan_results:
        summary += "Shodan Exposure: Exposed services detected\n"
        summary += f"  - {shodan_results}\n"
    
    # Breach Data
    breach_data = results_data.get('breach', {})
    if isinstance(breach_data, dict):
        breach_count = len(breach_data.get('breaches', []))
        paste_count = len(breach_data.get('pastes', []))
        if breach_count > 0:
            summary += f"Data Breaches: {breach_count} historical breaches found\n"
        if paste_count > 0:
            summary += f"Paste Dumps: {paste_count} credential dumps detected\n"
    
    # DNS/Subdomain Results
    dns_data = results_data.get('dns', {})
    if isinstance(dns_data, dict):
        subdomain_count = len(dns_data.get('subdomains', []))
        if subdomain_count > 0:
            summary += f"Subdomains: {subdomain_count} subdomains discovered\n"
        
        exposed_services = dns_data.get('exposed_services', [])
        if exposed_services:
            summary += f"Exposed Services: {len(exposed_services)} open ports detected\n"
    
    # Social Media Mentions
    reddit_count = len(results_data.get('reddit', []))
    twitter_count = len(results_data.get('twitter', []))
    if reddit_count > 0:
        summary += f"Reddit Mentions: {reddit_count} potentially relevant posts\n"
    if twitter_count > 0:
        summary += f"Twitter Mentions: {twitter_count} potentially relevant tweets\n"
    
    # Dark Web / Pastebin
    pastebin_count = len(results_data.get('pastebin', []))
    if pastebin_count > 0:
        summary += f"Pastebin Dumps: {pastebin_count} suspicious pastes found\n"
    
    darkweb_results = results_data.get('darkweb', '')
    if darkweb_results and "leak mentioning" in darkweb_results:
        summary += "Dark Web: Potential mentions detected\n"
    
    return summary

def generate_threat_report(brand, results_data):
    """
    Generate a comprehensive threat intelligence report
    """
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        return "OpenAI API key not configured for threat report generation."
    
    # Create detailed report prompt
    detailed_summary = prepare_detailed_summary(brand, results_data)
    
    prompt = f"""
    Generate a professional Threat Intelligence Report for "{brand}" based on the following reconnaissance data:

    {detailed_summary}

    Structure the report as follows:
    
    ## EXECUTIVE SUMMARY
    Brief overview of findings and overall risk level.
    
    ## KEY FINDINGS
    - Most critical discoveries
    - Immediate threats
    - Potential attack vectors
    
    ## DETAILED ANALYSIS
    - GitHub exposure analysis
    - Infrastructure vulnerabilities
    - Data breach history
    - Social media intelligence
    
    ## RISK ASSESSMENT
    Rate each category (High/Medium/Low) and explain reasoning.
    
    ## RECOMMENDATIONS
    - Immediate actions (0-30 days)
    - Short-term improvements (1-3 months)
    - Long-term strategy (3+ months)
    
    Keep the report professional and actionable for security teams.
    """
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-4',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a senior cybersecurity analyst creating threat intelligence reports. Write in a professional, technical tone suitable for security teams and management.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': 2000,
                'temperature': 0.2
            },
            timeout=45
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Error generating threat report: {response.status_code}"
            
    except Exception as e:
        return f"Error generating threat report: {str(e)}"

def prepare_detailed_summary(brand, results_data):
    """
    Prepare detailed summary with specific findings for threat report
    """
    summary = f"=== RECONNAISSANCE DATA FOR {brand.upper()} ===\n\n"
    
    # GitHub Analysis
    github_results = results_data.get('github', [])
    summary += f"GITHUB EXPOSURE:\n"
    summary += f"- {len(github_results)} potential code leaks identified\n"
    for i, result in enumerate(github_results[:3]):  # Top 3 results
        summary += f"  {i+1}. Repository: {result.get('repo', 'N/A')}\n"
        summary += f"     File: {result.get('path', 'N/A')}\n"
    
    # Infrastructure
    dns_data = results_data.get('dns', {})
    if isinstance(dns_data, dict):
        subdomains = dns_data.get('subdomains', [])
        summary += f"\nINFRASTRUCTURE:\n"
        summary += f"- {len(subdomains)} subdomains discovered\n"
        
        exposed_services = dns_data.get('exposed_services', [])
        if exposed_services:
            summary += f"- {len(exposed_services)} exposed services:\n"
            for service in exposed_services:
                summary += f"  * Port {service.get('port')}: {service.get('service')}\n"
    
    # Breach History
    breach_data = results_data.get('breach', {})
    if isinstance(breach_data, dict):
        breaches = breach_data.get('breaches', [])
        summary += f"\nBREACH HISTORY:\n"
        summary += f"- {len(breaches)} historical breaches found\n"
        for breach in breaches[:2]:  # Top 2 breaches
            summary += f"  * {breach.get('name')}: {breach.get('pwn_count', 0)} accounts\n"
    
    # Shodan Intelligence
    shodan_results = results_data.get('shodan', '')
    summary += f"\nSHODAN INTELLIGENCE:\n"
    summary += f"- {shodan_results}\n"
    
    # Social Media Intelligence
    reddit_results = results_data.get('reddit', [])
    twitter_results = results_data.get('twitter', [])
    summary += f"\nSOCIAL MEDIA INTELLIGENCE:\n"
    summary += f"- Reddit mentions: {len(reddit_results)}\n"
    summary += f"- Twitter mentions: {len(twitter_results)}\n"
    
    return summary

def get_security_score(brand, results_data):
    """
    Calculate a security score based on findings
    """
    score = 100  # Start with perfect score
    
    # Deduct points for various findings
    github_count = len(results_data.get('github', []))
    score -= github_count * 10  # 10 points per GitHub leak
    
    # Shodan exposure
    shodan_results = results_data.get('shodan', '')
    if "found on Shodan" in shodan_results:
        score -= 20
    
    # Breach history
    breach_data = results_data.get('breach', {})
    if isinstance(breach_data, dict):
        breach_count = len(breach_data.get('breaches', []))
        score -= breach_count * 15  # 15 points per breach
    
    # DNS exposure
    dns_data = results_data.get('dns', {})
    if isinstance(dns_data, dict):
        exposed_services = dns_data.get('exposed_services', [])
        score -= len(exposed_services) * 5  # 5 points per exposed service
    
    # Ensure score doesn't go below 0
    score = max(0, score)
    
    return {
        'score': score,
        'grade': 'A' if score >= 90 else 'B' if score >= 80 else 'C' if score >= 70 else 'D' if score >= 60 else 'F',
        'risk_level': 'Low' if score >= 80 else 'Medium' if score >= 60 else 'High'
    }