# Sustainable Architectural Design Decisions

Mar 09, 2014 17 min read

by

- [Rafael Capilla](https://www.infoq.com/profile/Rafael-Capilla/)
- [Olaf Zimmermann](https://www.infoq.com/profile/Olaf-Zimmermann/)



Software architects must create designs that can endure throughout software evolution. Today, software architecture comprises not only a system’s core structure but also essential design decisions.1,2 So, to achieve sustainable architectures, we need sustainable design decisions. In correspondence with Heiko Koziolek’s definition of architecture sustainability,3 we argue that architectural design decision sustainability involves

- the time period when the right and relevant decisions remain unchanged, and
- the cost efficiency of required changes to those decisions.

Although research has dealt with software architecture sustainability3 and corresponding evaluation methods,4 it hasn’t yet revealed how to make architectural design decisions sustainable. In more than 10 industrial projects and eight research projects, we’ve applied various techniques to yield sustainable architectural design decisions. Here, we describe the fruits of our experiences: the challenges to achieving sustainable decisions, the criteria for such decisions, the solutions we tried, and the lessons we learned.

## Challenges to Achieving Sustainable Decisions

Many researchers and practitioners consider architectural knowledge (AK) to be an inherent part of software design. They point to the importance of capturing significant architectural design decisions together with other software artifacts because those decisions can ensure that the design rationale doesn’t get lost.5 Capturing significant decisions and their rationale is difficult and often neglected because doing so requires considerable effort.6,7 In this context, architects should seek to make and document sustainable decisions. However, various challenges can hinder this desire.

## Decision Documentation Effort

A key challenge in various industrial cases is that the relatively high effort needed for design decision documentation6 often isn’t well accepted. Many decision templates require filling in 10 to 20 fields to document a single design decision. Although each documentation attribute is important, this documentation frequently takes too much effort, so architects on high-pressure projects often neglect it.7 Therefore, software architects and project managers tend to disregard such practices over time, leading to decision rationale erosion in the long term.

Another consequence of strained time for decision documentation is low-quality documentation. For example, if a decision’s rationale is “the end user wants it,” the documentation isn’t likely to be useful over time.

### Understanding the Links between Decisions and Other Software Artifacts

When documenting design decisions, it’s important to establish links to other software artifacts such as requirements and architecture designs. 8 However, although many architectural-decision-capturing templates implicitly mention requirements, establishing and maintaining the right set of traceability links between the decisions and other software artifacts is time-consuming and difficult. But as we’ll see, capturing the right set of links can help increase decisions’ sustainability.3

### Avoiding Repetitive Effort

Many decisions are based on existing AK in the project or field. For example, in many service-oriented architecture (SOA) projects, service proxies and adapters must integrate legacy systems, each with only a slightly different design. So, each proxy and adapter requires its own decisions, but many of them are similar. Instead of documenting each decision on its own, we would like to reuse the AK and work only with variations of individual decisions, reducing the documentation effort and allowing decisions to be based more on timeproven knowledge.

### Dealing with Invalid or Bad Rationales

Decision drivers and the pros and cons of alternatives, recommendations, and rationales are particularly relevant when you’re capturing design decisions. However, architects sometimes choose bad or invalid rationales, leading to decisions that can be questioned and hence are unsustainable. Consider this valid justification for the external stakeholders’ needs:

*Alternative A best meets user expectations and functional requirements as documented in user stories, use cases, and the business process model.*

Compare it to this poorly chosen justification:

*End users want it, but no evidence exists of a pressing business need.*

## Decision Sustainability Criteria

To define decision sustainability in detail, we derived five key criteria.

### Strategic

During decision making, someone looking at strategic consequences should consider things such as the decisions’ long-term impact—for example, future operations and maintenance effort.

### Measurable and Manageable

You can measure and evaluate a decision’s outcome over time according to objective criteria, ideally numeric ones (as, for instance, propagated by quality attribute scenarios and workshops4). Capturing all fine-grained decisions isn’t possible, so architects must limit the decisions’ granularity to a certain level of detail (such as creating a design class). This will lead to a more sustainable set of decisions and fewer traceability links. Moreover, limiting the number of dependencies between decisions reduces changes’ ripple effect.

### Achievable and Realistic

The rationale for fitting the solution to the problem should be chosen pragmatically and made explicit. For example, architects can indicate that they have taken care to avoid over- or underengineering (that is, they should apply the “good enough” approach).

### Rooted in Requirements

Decision making should be grounded in domain-specific architecting experience and context. It should take into account the company environment as well as project requirements and constraints, including the development team’s current skills, training budget, and process.

### Timeless

Decisions should be based on experience and knowledge that won’t likely be soon outdated. For example, architects can choose platform-neutral architectural patterns or tactics.

### Criteria Discussion

These five criteria strongly relate to the decision life cycle because software engineers need to track every change, regardless of whether the decisions are still valid.3 So, the decisions’ evolution across the life cycle clearly affects the degree of sustainability achieved at any time. Moreover, although not all these criteria apply to every decision, our experience shows that sustainable decisions often meet most of these criteria.

![img](https://imgopt.infoq.com/fit-in/3000x4000/filters:quality(85)/filters:no_upscale()/articles/sustainable-architectural-design-decisions/en/resources/table1.png)

## Solutions and Lessons Learned

Table 1 summarizes the lessons we learned from applying techniques for organizing, documenting, and evolving architectural design decisions. (We will discuss these in more detail later in this article.) Although these results are based on the various industry and research projects in which we’ve been involved, we focus here on one case from the COMPAS project: customer  relationship management (CRM) fulfillment.

In the case from the COMPAS project, a customer initiates CRM fulfillment by placing an order for an ISP’s services. The fulfillment process involves initializing the services, shipping the necessary equipment, charging the customer’s account, and sending the customer an invoice. It also incorporates functionality provided by three service-based platforms including CRM, billing, and ISP provisioning systems. The main company’s bundle of Internet and telecom services includes a network subscriber line, email addresses, Webbased administration, directory numbers, fax numbers, and voice-over-IP communication.

In the COMPAS project, we were confronted with short development iterations because working prototypes had to be delivered frequently. So, collecting all the requirements and delivering a full architecture design and documentation upfront wasn’t feasible. On the other hand, if important design decisions weren’t sustainable, they could impede continued development and integration. Central requirements for this project were to capture and document the relevant compliance requirements stemming from the relevant regulations and legislation, as well as the ISP’s business policies, and ensure that the systems complied with them.

### Initially Apply Lean, Minimalistic Decision Documentation

To reduce design documentation effort, we experimented with lean, minimalistic documentation. One approach was our (WH)Y approach (named for its Y-shaped visualization), inspired by George Fairbanks’s proposed documentation of design rationale.12 This approach reduces the documentation to a statement in this form:

*In the context of <use case/user story u>, facing <concern c> we decided for <option o> to achieve <quality q>, accepting <downside d>.*

Consider the following decision in the context of our CRM fulfillment example:

*In the context of* checking customer’s accounts and signing orders, facing that duties are not adequately segregated (SOX 404), *we decided to* ensure that customers’ accounts are verified by the financial department while the orders are checked and signed by the sales department to achieve proper segregation of duties, accepting that the order processing time is longer.

Another lean approach we used, [ADvISE9](https://swa.univie.ac.at/Architectural_Design_Decision_Support_Framework_(ADvISE))) (Architectural Design Decision Support Framework (ADvISE)), employs questionnaires to help architects focus on important decisions. Similar recurring decisions, which are tedious to document, can be captured through an automatically generated  questionnaire, which asks only essential questions about the recurring decision. So, we can document recurring decisions faster, reduce the burden of capturing AK, and produce a more sustainable set of decisions. In our experience, architects prefer using lean documentation rather than elaborate, large decision templates. On the other hand, people who are new to a project or set of decisions typically prefer to read the full-blown templates.

### Compile Guidance Models of Recurring Decisions

Recurring decisions are more timeproven than those that are used for the first time. To reduce effort in capturing recurring decisions on similar projects, we introduced guidance models to record decisions from previous projects and derive decision instances from the recurring ones.7 In our experience, the effort reduction gained from documenting recurring decisions and the improved quality through reuse lead to more accurate decision documentation and less maintenance effort. However, this approach requires an initial investment for creating the guidance model, and it’s not applicable for completely new decisions.

As an example, Table 2 shows part of a guidance model for SOAs we used in various projects—for instance, for developing the three service-based platforms in our CRM fulfillment example.7 Because these platforms are based on SOAs and de facto standards and technologies such as WSDL (Web Services Description Language), SOAP, REST (Representational State Transfer), SCA (Service Component Architecture), and .NET, we benefited from a high degree of reusability of the other guidance models.7 (Additional examples and evidence for this solution are in Software Architecture Knowledge Management: Theory and Practice.1)

![img](https://imgopt.infoq.com/fit-in/3000x4000/filters:quality(85)/filters:no_upscale()/articles/sustainable-architectural-design-decisions/en/resources/table2.png)

### Reuse Existing AK

Much AK is codified as well-known design patterns, corporate knowledge, or proven practices. For example, in the guidance model of Table 2, we used a significant number of patterns for our key design decisions. Our experience shows that such codified AK eases the creation of a guidance model that compiles proven design solutions. Regarding corporate knowledge, many companies, for example, require software architects to document a significant amount of information regarding compliance with national and international regulations such as Basel II or the Sarbanes-Oxley Act, internal business policies, or the rationale of such knowledge.10 In our observations, capturing and maintaining relationships between sources and architectural design decision rationales can prevent AK’s vaporization, helping it endure throughout the decision’s lifetime. Figure 1, which is from the CRM fulfillment example, shows how to minimize decision documentation effort by reusing domain-specific knowledge.10

![img](https://imgopt.infoq.com/fit-in/3000x4000/filters:quality(85)/filters:no_upscale()/articles/sustainable-architectural-design-decisions/en/resources/3Fig3.png)

**Figure 1. Reusing domain-specific knowledge. (a) A compliance model documented for legal purposes that links compliance controls in the account management service and the customer relations management (CRM) system to compliance requirements and risks stemming from EU Directive 95/46/EC on data protection for individuals. (b) Parts of the decision template automatically extracted from the model.**

### Establish Explicit Traceability Links between Decisions and Requirements

Many software maintenance tasks need well-documented design decisions to model explicit traceability links between decisions and requirements.
Although existing traceability approaches are valid attempts to support this goal,8 maintaining a large number of links is difficult. However, you can avoid this by explicitly specifying required links. For example, you can check all use cases for architecturally significant requirements and all architectural decisions to ensure no link is forgotten. The (WH)Y approach can help because it explicitly relates requirements as an influential factor of the architectural rationale, in the form of either a use case or user story.

The example of checking customers’ accounts and signing the orders (see the section “Initially Apply Lean, Minimalistic Decision Documentation”) describes a use case of the system we wanted to build. Similarly, the compliance model in Figure 1a explicitly links every decision for a compliance control to a compliance requirement. Because each control can be interpreted as one decision, a direct link exists between decisions and requirements. Explicit traceability links between decisions and requirements significantly enhance the understanding of decisions in relation to relevant requirements and increase the capability of adapting to certain requirements changes. So, the traceability links reduced maintenance effort in our projects and reinforced the delivered systems’ sustainability.

### Establish Traceability Links among Decisions, Architecture, and Code

Developers and architects often neglect the traceability links among decisions, architectural design, and code. So, it’s difficult to efficiently analyze and understand particular changes’ effects before implementing and deploying them.8 Moreover, code changes could cause design or decision documentation to become invalid or inconsistent with the implemented system. Therefore, these links’ sustainability greatly affects the architecture’s sustainability. In our experience, sustainable sets of traceability links are best established semiautomatically. Manually establishing them is too much work, and fully automated approaches often lead to many inaccurate or imprecise links that won’t last.

Consider the view-based, modeldriven traceability approach (VbTrace)11 used in our CRM fulfillment example as an extension of the View-based Modeling
Framework (VbMF),11 which establishes relationships among the different software artifacts at different granularity and abstraction levels (for example, architectural-view models and code). These relationships are generated automatically using model-driven techniques from manually specified models.
The combination of VbTrace and guidance models helps define the dependencies between AK and architectures semiautomatically. So, the evolution of
changes can be better controlled sustainably with less effort.

For instance, to deploy the CRM system in Europe, we needed to adapt it to conform to EU Directive 95/46/EC (see Figure 1). We identified all the use cases containing interactions with external actors (such as customers) and the corresponding design decisions. We could analyze the decisions’ effects on the design artifacts and code modules using ADvISE’s AK-to-architectural-models relationships9 and VbTrace’s model-to-model and modelto-implementation
traceability links.11

### Follow Rationale Guidelines

From analyzing many rationales in our projects, we learned that rationales should follow three guidelines. First, they should be precise and avoid commonsense statements, truisms, and “killer phrases” (defensive, negative, or pejorative phrases). Second, they should highlight decision drivers (a desired system quality such as subsecond response time) and explain why recommendations in guidance models or other trusted sources were or weren’t
followed. Finally, they should refer to actual project requirements, not just generic background information from the literature. More rationale guidelines
can be found elsewhere.13 Our approach goes a step beyond the knowledge-capturing problem because we explicitly provide guidelines to identify
and capture a minimalistic set of relevant decisions and trace links that make the decisions more sustainable than previous approaches have. If you follow this approach (see the sidebar “Guidelines to Achieve Sustainable Decisions”), you won’t waste effort on simplistic or unimportant decisions, but you’ll still present important and more complex decisions with sufficient detail. The major effort of decision documentation will be taken out of the daily work flow during development, but all decisions will still be recorded minimally to ensure no important decisions are forgotten. We plan to provide precise cost and
effort estimations from the projects we’ve worked on to show how our approach improves sustainability during mid- to long-term system evolution.

## Guidelines to Achieve Sustainable Decisions

We learned the following lessons in our work that can serve as guidelines and assessment for achieving sustainable decisions:

1. Use a lean/minimalistic approach for the initial decision documentation.
2. Prioritize and capture all important decisions that are relevant enough for documenting and understanding the target architecture.
3. Detail the particularly important decisions with full-blown templates only after the initial work has been done (that is, when the decision makers are content with the architectural decisions made and confident that these decisions don’t have to be revised any time soon).
4. Use the lean/minimalistic versions from step 1 as a short version of documented decisions with the right granularity level to provide an overview of the detailed decisions, as well as for trivial or obvious decisions.
5. Wherever possible, use existing architectural knowledge, either from guidance models or from other sources. Review and extend such knowledge and fit it to the context of the specific decision.
6. Ensure that traceability links are established between decisions and both requirements and architectural designs/code. Provide automated consistency checking to make sure the traceability links are in sync after a change. Limit the number of dependencies between decisions and other software artifacts.
7. Apply the guidelines for the justifications consequently and forcefully—they’re the most important part of the decision documentation because they give the rationale.

## References

1 M.A. Babar et al., Software Architecture Knowledge Management: Theory and Practice, Springer, 2009.
2 A.H. Dutoit et al., Rationale Management in Software Engineering, Springer, 2006.
3 H. Koziolek, “Sustainability Evaluation of Software Architectures: A Systematic Review,” Proc. Joint ACM SIGSOFT Conf.—QoSA and ACM SIGSOFT Symp.—ISARCS on Quality of Software Architectures—QoSA and Architecting Critical Systems—ISARCS, ACM, 2011, pp. 3–12.
4 P. Clements, R. Kazman, and M. Klein, Evaluating Software Architectures: Methods and Case Studies, Addison-Wesley, 2001.
5 A. Jansen and J. Bosch, “Software Architecture as a Set of Architectural Design Decisions,” Proc. 5th Working IEEE/IFIP Conf. Software Architecture, IEEE CS, 2005, pp. 109–120.
6 R. Capilla, F. Nava, and C. Carrillo, “Effort Estimation in Capturing Architectural Knowledge,” Proc. 23rd Conf. Automated Software Eng. (ASE 08), IEEE CS, 2008, pp. 208–217.
7 O. Zimmermann et al., “Combining Pattern Languages and Reusable Architectural Decision Models into a Comprehensive and Comprehensible Design Method,” Proc. 7th Working IEEE/IFIP Conf. Software Architecture, IEEE CS, 2008, pp. 157–166.
8 M. Galster, “Dependencies, Traceability and Consistency in Software Architecture: Towards a View-Based Perspective,” Proc. 5th European Conf. Software Architecture: Companion Vol. (ECSA 11), ACM, 2011, article 1.
9 I. Lytra, H. Tran, and U. Zdun, “Constraint-Based Consistency Checking between Design Decisions and Component Models for Supporting Software Architecture Evolution,” Proc. 16th European Conf. Software Maintenance and Reengineering (CSMR 12), IEEE CS, 2012, pp. 287–296.
10 H. Tran, I. Lytra, and U. Zdun, “Derivation of Domain-Specific Architectural Knowledge Views from Governance and Security Compliance Metadata,” Proc. 28th ACM Symp. Applied Computing (SAC 13), ACM, 2013, pp. 1728–1733.
11 H. Tran, U. Zdun, and S. Dustdar, “VbTrace: Using View-Based and Model-Driven Development to Support Traceability in Process-Driven SOAs,” Software and Systems Modeling, vol. 10, no. 1, 2011, pp. 5–29.
12 G. Fairbanks, Just Enough Software Architecture: A Risk-Driven Approach, Marshall & Brainerd, 2010.
13 O. Zimmermann, N. Schuster, and P. Eeles, Modeling and Sharing Architectural Decisions, Part 1: Concepts, IBM developerWorks, 2008.