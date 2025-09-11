## 📊 Step {{ step_number }} Results

{% if passed %}
### ✅ Validation Successful!

Great job! All checks have passed for this step.
{% else %}
### ❌ Validation Failed

Some checks didn't pass. Please review the feedback below and try again.
{% endif %}

### 📋 Results Summary
{{ results_table }}

{% if tips %}
### 💡 Tips for Success
{% for tip in tips %}
- {{ tip }}
{% endfor %}
{% endif %}

---
*Powered by automated testing*