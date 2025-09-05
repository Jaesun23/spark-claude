---
name: spark-design
description: System design and UI/UX creation with architecture expertise focusing on scalability and accessibility
type: command
requires: designer-spark
---

# /spark-design - Intelligent Design Command

**Purpose**: Design is the art of making the complex simple and the invisible visible, creating solutions that feel inevitable once you see them.

## Philosophy (Natural Language Inspiration)

Great design is invisible until it's missing. We approach design with:

- **User-centered thinking**: Every decision serves the end user experience
- **Systematic consistency**: Patterns that create familiarity and trust
- **Accessible by default**: Inclusive design that works for everyone
- **Scalable foundations**: Designs that grow gracefully with needs

Design is both art and engineering - beautiful solutions that solve real problems elegantly.

## Behavior Protocol (Code-Based Execution)

```python
class SparkDesignCommand:
    """Intelligent design with systematic architecture and user experience focus.
    
    This protocol ensures design consistency while the philosophy above
    inspires user-centered solutions. Together they create lasting value.
    """
    
    # Design dimensions - HOLISTIC APPROACH
    DESIGN_AREAS = {
        "system_architecture": ["scalability", "maintainability", "security"],
        "user_interface": ["accessibility", "responsiveness", "usability"],
        "data_design": ["schema", "relationships", "performance"],
        "api_design": ["REST", "GraphQL", "documentation"]
    }
    
    # Quality standards - NON-NEGOTIABLE
    DESIGN_STANDARDS = {
        "accessibility_compliance": "WCAG 2.1 AA",
        "mobile_first": True,
        "performance_budget": {"lcp": "2.5s", "cls": "0.1"},
        "scalability_tested": True
    }
    
    def create_design(self, requirements: dict) -> dict:
        """Main design creation with systematic approach."""
        design_context = self.analyze_requirements(requirements)
        
        # Design in layers from foundation up
        foundation = self.design_system_foundation(design_context)
        components = self.design_components(foundation, design_context)
        integration = self.design_integration_points(components)
        
        # Validate against all standards
        validation = self.validate_design_standards(
            foundation, components, integration
        )
        
        if not validation["passes_all_checks"]:
            refined_design = self.refine_design_based_on_validation(
                validation["issues"]
            )
            return refined_design
        
        return self.finalize_design_deliverables(
            foundation, components, integration
        )
    
    def balance_aesthetics_with_function(self, context: dict) -> str:
        """Balance beautiful design with practical functionality.
        
        Embodies '미묘한 조절이나 균형의 묘' - knowing when beauty
        serves function versus when simplicity is more elegant.
        """
        if context["user_expertise"] == "beginner":
            return "simplicity_focused"
        elif context["feature_complexity"] == "high":
            return "clarity_focused"
        else:
            return "balanced_design"
```

## 📝 2호(Claude Code) MUST FOLLOW THIS EXACT PROTOCOL

### **WHEN RECEIVING /spark-design COMMAND:**

```python
1. IMMEDIATELY CALL:
   Task("designer-spark", user_request)

2. WAIT for agent completion

3. CHECK ~/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - output.files.created is not empty OR output.docs.api == true
   - state.status == "completed"

4. DECISION:
   ✅ ALL CONDITIONS MET → Report design complete to user
   ❌ ANY CONDITION FAILED → Task("designer-spark", "Complete the design: {issues}")
```

The designer-spark specialist will:
- Create comprehensive system architectures and UI/UX designs
- Apply mobile-first and accessibility-first principles
- Design scalable solutions with performance optimization
- Follow modern design patterns and best practices
- Deliver production-ready components and specifications

## Usage Examples

```bash
/spark-design "create responsive dashboard component with real-time data"
/spark-design "design system architecture for microservices application"  
/spark-design "build accessible form components following WCAG 2.1"
/spark-design "create mobile-first navigation component"
/spark-design "design database schema for e-commerce platform"
```

## Design Capabilities

- **UI Components**: Responsive, accessible React/Vue/HTML components  
- **System Architecture**: Scalable system design with clear separation of concerns
- **Database Design**: Optimized schemas with proper relationships and indexing
- **API Design**: RESTful and GraphQL APIs following OpenAPI standards
- **User Experience**: Mobile-first, accessibility-focused design patterns

## Design Standards

All SPARK designs ensure:
- ✅ **Responsive Design**: Mobile-first approach with all screen sizes supported
- ✅ **Accessibility**: WCAG 2.1 AA compliance with semantic HTML and ARIA
- ✅ **Performance**: Optimized loading, minimal bundle size, efficient rendering
- ✅ **Scalability**: Designs that work from prototype to enterprise scale
- ✅ **Consistency**: Follows established design systems and patterns

## SPARK Intelligence Integration

- 🎭 **Frontend/Architect Persona**: Activates design-focused thinking
- 🎨 **Modern Patterns**: Uses current best practices and design systems
- ♿ **Accessibility First**: Built-in WCAG compliance and inclusive design
- 🚀 **Optimized Token Usage**: Efficient design creation without bloat