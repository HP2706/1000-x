import streamlit as st
import numpy as np

def simulate_one_scenario(n_people, n_industries, rate_of_improvement, learning_cap, knowledge_decay, years_worked_per_job):
    improvements = np.zeros(shape=n_people)
    for i in range(n_people):
        work_distb = years_worked_per_job[i]
        max_improvement = rate_of_improvement**work_distb * knowledge_decay ** work_distb
        capped_improvement = np.minimum(max_improvement, learning_cap)
        improvements[i] = np.prod(capped_improvement)
    return improvements

def main():
    st.title('Can you become 1000x')
    st.markdown('[Inspired by a blog post i wrote, on the distribution in capabilities of people](https://majestic-burrito-31e.notion.site/how-you-become-1000x-f646edf647b34c47b0f66167c10bc5eb?pvs=4)')

    # Sidebar for parameters
    n_people = st.sidebar.number_input('Number of People', min_value=1000, max_value=20000, value=10000)
    n_industries = st.sidebar.number_input('Number of Industries', min_value=10, max_value=200, value=100)
    max_improvement = st.sidebar.number_input('Maximum annual Improvement', min_value=1.0, max_value=5.0, value=1.5)
    max_learning_cap = st.sidebar.number_input('Learning Cap(absolute)', min_value=1.0, max_value=10.0, value=2.0)
    max_knowledge_decay = st.sidebar.number_input('Annual Knowledge Decay(smaller is "larger")', min_value=0.0, max_value=1.0, value=0.9)
    max_years_worked = st.sidebar.number_input('Maximum Years Worked', min_value=20, max_value=80, value=60)

    # Simulate button
    if st.button('Simulate'):
        # Define parameters
        rate_of_improvement = np.random.uniform(1, max_improvement, n_industries)  # Rate of improvement per industry
        learning_cap = np.random.uniform(1, max_learning_cap , n_industries)  # Learning cap per industry
        knowledge_decay = np.random.uniform(max_knowledge_decay, 1, n_industries)  # Knowledge decay per industry


        years_worked = np.random.randint(20, 80, n_people) # Years worked per person
        years_worked_per_job = np.zeros(shape=(n_people, n_industries))
  
        for i in range(n_people):
            non_zero_count = np.random.randint(1, 10)  # Randomly choose how many values will be non-zero
            dirichlet_sample = np.random.dirichlet(np.ones(non_zero_count), size=1)[0]
            indices = np.random.choice(n_industries, non_zero_count, replace=False)  # Choose where to place the non-zero values
            sparse_distribution = np.zeros(n_industries)
            sparse_distribution[indices] = dirichlet_sample
            years_worked_per_job[i] = years_worked[i] * sparse_distribution


        out = simulate_one_scenario(n_people, n_industries, rate_of_improvement, learning_cap, knowledge_decay, years_worked_per_job)
        absolute_sorted = np.sort(out)
        max_improvement = np.max(out)
        # Display results

        # Plot for Absolute Improvement
        st.header('Absolute Improvement')
        st.line_chart(absolute_sorted)

        # get top 10% "ownership"
        top_10_percent = np.sum(absolute_sorted[int(n_people * 0.1):])
        st.header('Top 10% share of total improvement')
        st.write(top_10_percent/np.sum(absolute_sorted))

        mean_improvement = np.mean(out)
        st.header('Improvement / mean improvement')
        normalized = out / mean_improvement
        normalized_sorted = np.sort(normalized)
        st.line_chart(normalized_sorted)
        
if __name__ == '__main__':
    main()