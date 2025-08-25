# /spark-design - SPARK Design Command

**Purpose**: System design and UI/UX creation with architecture and accessibility expertise

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